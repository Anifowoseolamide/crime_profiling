import logging
from rest_framework import generics, permissions
from .models import WantedPerson
from .serializers import WantedPersonSerializer
from audit.mixins import AuditLogMixin

logger = logging.getLogger(__name__)

class IsSupervisorOrAdminForCreate(permissions.BasePermission):
    """
    Field officers can view the wanted list but only
    supervisors/admins can issue new warrants.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role in ['SUPERVISOR', 'ADMIN']

class WantedListView(AuditLogMixin, generics.ListCreateAPIView):
    """
    GET /api/wanted/
    POST /api/wanted/ (Supervisors/Admins only)
    """
    serializer_class = WantedPersonSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupervisorOrAdminForCreate]
    audit_action = 'WANTED_ADDED'
    audit_target_type = 'WantedPerson'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"WANTED VALIDATION ERROR: {serializer.errors}")
            logger.error(f"PAYLOAD RECEIVED: {request.data}")
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        qs = WantedPerson.objects.select_related('subject', 'created_by').order_by('-priority', '-issued_date')
        params = self.request.query_params
        
        if is_active := params.get('is_active'):
            qs = qs.filter(is_active=is_active.lower() == 'true')
        if priority := params.get('priority'):
            qs = qs.filter(priority=priority)
        if subject_id := params.get('subject_id'):
            qs = qs.filter(subject_id=subject_id)
            
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        self.write_audit_log(instance, extra_meta={'warrant_number': instance.warrant_number})


class WantedDetailView(AuditLogMixin, generics.RetrieveUpdateAPIView):
    """
    GET /api/wanted/{id}/
    PATCH /api/wanted/{id}/ (Supervisors/Admins only)
    """
    queryset = WantedPerson.objects.select_related('subject', 'created_by')
    serializer_class = WantedPersonSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupervisorOrAdminForCreate]
    audit_action = 'WANTED_UPDATED'
    audit_target_type = 'WantedPerson'
