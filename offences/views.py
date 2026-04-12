import logging
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Offence
from .serializers import (
    OffenceListSerializer, 
    OffenceDetailSerializer, 
    OffenceUpdateStatusSerializer
)
from audit.mixins import AuditLogMixin

logger = logging.getLogger(__name__)

class IsSupervisorOrAdminForStatus(permissions.BasePermission):
    """
    Field officers can view and create offences, but only 
    Supervisors+ can update an offence's status or penalty.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return True
        # For PUT/PATCH/DELETE
        return request.user.role in ['SUPERVISOR', 'ADMIN']

class OffenceListView(AuditLogMixin, generics.ListCreateAPIView):
    """
    GET /api/offences/
    POST /api/offences/
    """
    permission_classes = [permissions.IsAuthenticated]
    audit_action = 'OFFENCE_CREATED'
    audit_target_type = 'Offence'
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OffenceDetailSerializer
        return OffenceListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"OFFENCE VALIDATION ERROR: {serializer.errors}")
            logger.error(f"PAYLOAD RECEIVED: {request.data}")
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        qs = Offence.objects.select_related('subject', 'arresting_officer', 'station').order_by('-incident_date')
        params = self.request.query_params
        
        if subject_id := params.get('subject_id'):
            qs = qs.filter(subject_id=subject_id)
        if category := params.get('offence_category'):
            qs = qs.filter(offence_category=category)
        if severity := params.get('severity'):
            qs = qs.filter(severity=severity)
        if status := params.get('status'):
            qs = qs.filter(status=status)
        if station_id := params.get('station_id'):
            qs = qs.filter(station_id=station_id)
            
        return qs

    def perform_create(self, serializer):
        # We assume station is provided in request or we infer from officer
        officer = self.request.user
        
        # Prepare extra data for the model
        extra_data = {}
        
        # Assign current user as arresting officer if not provided
        if not serializer.validated_data.get('arresting_officer_id'):
            extra_data['arresting_officer'] = officer
            
        # Assign station: use provided station_id, or officer's station, or fallback
        if not serializer.validated_data.get('station_id'):
            if officer.station:
                extra_data['station'] = officer.station
            else:
                from authentication.models import PoliceStation
                fallback_station = PoliceStation.objects.first()
                if fallback_station:
                    extra_data['station'] = fallback_station
        
        offence = serializer.save(**extra_data)
        
        # Atomically update subject location
        update_fields = {}
        if offence.location: 
            update_fields['last_known_location'] = offence.location
        if offence.latitude is not None: 
            update_fields['last_known_lat'] = offence.latitude
        if offence.longitude is not None: 
            update_fields['last_known_lng'] = offence.longitude
            
        if update_fields:
            if offence.incident_date:
                update_fields['last_seen_date'] = offence.incident_date
            else:
                from django.utils import timezone
                update_fields['last_seen_date'] = timezone.now()
            from subjects.models import Subject
            Subject.objects.filter(pk=offence.subject.pk).update(**update_fields)

class OffenceDetailView(AuditLogMixin, generics.RetrieveUpdateAPIView):
    """
    GET /api/offences/{id}/
    PATCH /api/offences/{id}/ (Restricted to supervisors)
    """
    queryset = Offence.objects.select_related('subject', 'arresting_officer', 'station')
    permission_classes = [permissions.IsAuthenticated, IsSupervisorOrAdminForStatus]
    audit_action = 'OFFENCE_UPDATED'
    audit_target_type = 'Offence'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            # For simplicity, if we want full edit we could use OffenceDetailSerializer
            # But the spec says "Update Offence Status". We'll allow full update for admins
            # but usually it's just status update. We'll use OffenceUpdateStatusSerializer
            # to strictly follow the "supervisors can update status" requirement.
            if self.request.user.role == 'ADMIN':
                return OffenceDetailSerializer
            return OffenceUpdateStatusSerializer
        return OffenceDetailSerializer
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Log view access
        self.audit_action = 'OFFENCE_VIEWED'
        self.write_audit_log(instance)
        self.audit_action = 'OFFENCE_UPDATED' # reset
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CrimeHotspotView(APIView):
    """
    GET /api/offences/hotspots/
    Aggregates offences by location to generate hotspot clusters.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        offences = Offence.objects.filter(
            latitude__isnull=False, longitude__isnull=False
        ).values('location', 'latitude', 'longitude', 'severity')
        
        severity_rank = {
            'CAPITAL': 5,
            'VIOLENT': 4,
            'SERIOUS': 3,
            'MODERATE': 2,
            'MINOR': 1
        }
        
        # Fallback if the choices in model are different (model has MINOR, MODERATE, SERIOUS, VIOLENT, CAPITAL)
        hotspots = {}
        for off in offences:
            loc = off['location']
            if loc not in hotspots:
                hotspots[loc] = {
                    'name': loc,
                    'lat': off['latitude'],
                    'lng': off['longitude'],
                    'count': 0,
                    'severity': off['severity'],
                    '_rank': severity_rank.get(off['severity'], 1)
                }
            
            hotspots[loc]['count'] += 1
            curr_rank = severity_rank.get(off['severity'], 1)
            if curr_rank > hotspots[loc]['_rank']:
                hotspots[loc]['_rank'] = curr_rank
                hotspots[loc]['severity'] = off['severity']
                
        result = []
        for h in hotspots.values():
            del h['_rank']
            result.append(h)
            
        # Frontend map expects severity as HIGH/MEDIUM/LOW
        # Map them before returning
        severity_mapping = {
            'CAPITAL': 'HIGH',
            'VIOLENT': 'HIGH',
            'SERIOUS': 'HIGH',
            'MODERATE': 'MEDIUM',
            'MINOR': 'LOW'
        }
        
        for h in result:
            h['severity'] = severity_mapping.get(h['severity'], 'LOW')
            
        return Response(result)
