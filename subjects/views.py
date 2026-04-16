from django.db.models import Count, Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import logging
import base64
import cloudinary.uploader

logger = logging.getLogger(__name__)

from django.conf import settings
from .models import Subject, Mugshot
from .serializers import SubjectListSerializer, SubjectDetailSerializer, MugshotSerializer
from services.compreface import compreface
from services.faceplusplus import faceplusplus
from audit.mixins import AuditLogMixin


class SubjectListView(AuditLogMixin, generics.ListCreateAPIView):
    """
    GET /api/subjects/ — List & search subjects
    POST /api/subjects/ — Create new subject profile (Supervisor/Admin)
    """
    audit_action = 'SUBJECT_CREATED'
    audit_target_type = 'Subject'
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubjectDetailSerializer
        return SubjectListSerializer
        
    def get_permissions(self):
        if self.request.method == 'POST':
            # Only supervisors+ can create manual profiles without an identification flow
            return [permissions.IsAuthenticated()]  # Can restrict further using custom permissions
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = Subject.objects.prefetch_related('mugshots').annotate(
            offence_count=Count('offences')
        ).order_by('-created_at')
        
        params = self.request.query_params
        if search := params.get('search'):
            qs = qs.filter(
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search) | 
                Q(aliases__icontains=search)
            )
        if risk := params.get('risk_level'):
            qs = qs.filter(risk_level=risk)
        if stat := params.get('status'):
            qs = qs.filter(status=stat)
        if wanted := params.get('is_wanted'):
            wanted_bool = wanted.lower() == 'true'
            if wanted_bool:
                qs = qs.filter(status='WANTED')
                
        return qs

class SubjectDetailView(AuditLogMixin, generics.RetrieveUpdateAPIView):
    """
    GET/PUT/PATCH /api/subjects/{id}/
    """
    queryset = Subject.objects.prefetch_related('mugshots')
    serializer_class = SubjectDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    audit_action = 'SUBJECT_UPDATED'
    audit_target_type = 'Subject'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Log that the officer viewed the profile
        self.audit_action = 'SUBJECT_VIEWED'
        self.write_audit_log(instance)
        self.audit_action = 'SUBJECT_UPDATED' # Reset for update operations
        
        return Response(serializer.data)


class SubjectMugshotUploadView(AuditLogMixin, APIView):
    """
    POST /api/subjects/{id}/enrol-mugshot/
    Uploads base64 image to Cloudinary, enrols in CompreFace, creates Mugshot record.
    """
    permission_classes = [permissions.IsAuthenticated]
    audit_action = 'MUGSHOT_ENROLLED'
    audit_target_type = 'Subject'
    
    def post(self, request, pk):
        try:
            subject = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
            
        base64_img = request.data.get('image')
        is_primary = request.data.get('is_primary', False)
        
        if not base64_img:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # 1. Decode image (basic validation)
            if ',' in base64_img:
                base64_img = base64_img.split(',')[1]
            img_bytes = base64.b64decode(base64_img)
            
            # 2. Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                f"data:image/jpeg;base64,{base64_img}",
                folder=f"lagoscp/subjects/{subject.id}/mugshots"
            )
            image_url = upload_result.get('secure_url')
            
            # 3. Enrol in Face Recognition Provider
            if settings.FACE_RECOGNITION_PROVIDER == 'facepp':
                faceplusplus.enrol_subject(subject.face_recognition_id, img_bytes)
            else:
                compreface.enrol_subject(subject.face_recognition_id, img_bytes)
            
            # 4. Save to DB
            mugshot = Mugshot.objects.create(
                subject=subject,
                image_url=image_url,
                is_primary=is_primary,
                captured_by=request.user,
                enrolled_in_face_recognition=True,
                latitude=request.data.get('latitude'),
                longitude=request.data.get('longitude')
            )
            
            # 5. Log activity
            self.write_audit_log(subject, extra_meta={
                'mugshot_id': str(mugshot.id), 
                'url': image_url,
                'latitude': mugshot.latitude,
                'longitude': mugshot.longitude
            })
            
            serializer = MugshotSerializer(mugshot)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.exception(f"Error enrolling mugshot for subject {pk}:")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubjectTimelineView(APIView):
    """
    GET /api/subjects/{id}/timeline/
    Aggregates Offence, IdentificationLog, and WantedPerson records for a subject into a unified chronological timeline.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            subject = Subject.objects.get(pk=pk)
        except Subject.DoesNotExist:
            return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

        from offences.models import Offence
        from identification.models import IdentificationLog
        from wanted.models import WantedPerson
        import datetime

        timeline = []
        
        offences = Offence.objects.filter(subject=subject)
        for off in offences:
            timeline.append({
                'type': 'OFFENCE',
                'date': off.incident_date or off.reported_date,
                'notes': off.offence_title,
                'location': off.location
            })
            
        logs = IdentificationLog.objects.filter(subject=subject)
        for log in logs:
            timeline.append({
                'type': 'SIGHTING' if log.match_found else 'SCAN',
                'date': log.timestamp,
                'notes': f"Match confidence: {round(log.confidence_score * 100, 2)}%" if log.confidence_score else "Scan",
                'location': log.location
            })
            
        warrants = WantedPerson.objects.filter(subject=subject)
        for war in warrants:
            date_val = war.issued_date or war.created_at
            # If date_val is just a date, convert to datetime for sorting
            if type(date_val) is datetime.date:
                from django.utils import timezone
                date_val = datetime.datetime.combine(date_val, datetime.time.min, tzinfo=timezone.get_current_timezone())
                
            timeline.append({
                'type': 'WARRANT',
                'date': date_val,
                'notes': war.reason,
                'location': ''
            })

        timeline = [t for t in timeline if t['date'] is not None]
        timeline.sort(key=lambda x: x['date'], reverse=True)
        
        return Response(timeline)
