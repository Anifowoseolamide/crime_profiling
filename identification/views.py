import base64
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import cloudinary.uploader
from django.db.models import Count
from django.utils import timezone

from .models import IdentificationLog
from .serializers import IdentificationLogSerializer, IdentifyRequestSerializer
from subjects.models import Subject
from subjects.serializers import SubjectListSerializer
from wanted.models import WantedPerson
from offences.models import Offence
from django.conf import settings
from services.compreface import compreface
from services.faceplusplus import faceplusplus
from audit.mixins import AuditLogMixin


class IdentifyView(AuditLogMixin, APIView):
    """
    POST /api/identify/
    Takes a field photo, queries CompreFace, returns full subject profile + alerts.
    """
    permission_classes = [permissions.IsAuthenticated]
    audit_action = 'SUBJECT_IDENTIFIED'
    audit_target_type = 'IdentificationLog'

    def post(self, request):
        serializer = IdentifyRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        base64_img = data['image']
        
        try:
            # 1. Decode & Upload to Cloudinary to save evidence of scan
            if ',' in base64_img:
                base64_img = base64_img.split(',')[1]
            img_bytes = base64.b64decode(base64_img)
            
            upload_result = cloudinary.uploader.upload(
                f"data:image/jpeg;base64,{base64_img}",
                folder="lagoscp/field_scans"
            )
            field_image_url = upload_result.get('secure_url')
            
            # 2. Query Face Recognition Provider
            if settings.FACE_RECOGNITION_PROVIDER == 'facepp':
                fr_result = faceplusplus.identify(img_bytes)
            else:
                fr_result = compreface.identify(img_bytes)
            
            # 3. Lookup Subject & Build Response
            subject = None
            is_wanted = False
            warrant_data = None
            offence_summary = None
            
            if fr_result['match_found'] and fr_result['subject_id']:
                subject = Subject.objects.filter(face_recognition_id=fr_result['subject_id']).first()
                
            match_actually_found = subject is not None
            
            # 4. Create Identification Log
            log = IdentificationLog.objects.create(
                officer=request.user,
                subject=subject,
                field_image_url=field_image_url,
                match_found=match_actually_found,
                confidence_score=fr_result['confidence'],
                face_recognition_response=fr_result['raw'],
                location=data.get('location', ''),
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                notes=data.get('notes', ''),
                device_id=data.get('device_id', '')
            )
            
            # 5. Write audit log
            audit_meta = {'confidence': fr_result['confidence']}
            if not match_actually_found:
                self.audit_action = 'FAILED_IDENTIFICATION'
                
            self.write_audit_log(log, extra_meta=audit_meta)
            
            # 6. Gather rich context if matched
            if match_actually_found:
                # Atomically update subject tracking coordinates
                update_fields = {'last_seen_date': timezone.now()}
                if data.get('location'): 
                    update_fields['last_known_location'] = data.get('location')
                if data.get('latitude') is not None: 
                    update_fields['last_known_lat'] = data.get('latitude')
                if data.get('longitude') is not None: 
                    update_fields['last_known_lng'] = data.get('longitude')
                
                Subject.objects.filter(pk=subject.pk).update(**update_fields)
                
                # REFRESH the subject instance to ensure we return the new coordinates
                subject.refresh_from_db()
                
                # Check for active warrants
                active_warrant = WantedPerson.objects.filter(
                    subject=subject, is_active=True
                ).order_by('-priority', '-issued_date').first()
                
                if active_warrant:
                    is_wanted = True
                    # Force synchronize subject status if it fell out of sync
                    if subject.status != 'WANTED':
                        subject.status = 'WANTED'
                        subject.save(update_fields=['status'])
                        
                    warrant_data = {
                        'warrant_number': active_warrant.warrant_number,
                        'reason': active_warrant.reason,
                        'priority': active_warrant.priority,
                        'issuing_authority': active_warrant.issuing_authority,
                        'issued_date': active_warrant.issued_date
                    }
                elif subject.status == 'WANTED':
                    # If they are marked WANTED but have NO active warrant records, 
                    # we might want to downgrade them to ACTIVE (optional safety check)
                    pass
                    
                # Summarise offences
                total_offences = Offence.objects.filter(subject=subject).count()
                open_cases = Offence.objects.filter(subject=subject, status__in=['OPEN', 'UNDER_INVESTIGATION']).count()
                most_recent = Offence.objects.filter(subject=subject).order_by('-incident_date').first()
                
                offence_summary = {
                    'total_offences': total_offences,
                    'open_cases': open_cases,
                    'most_recent': most_recent.incident_date if most_recent else None
                }
                
                return Response({
                    'match_found': True,
                    'confidence': fr_result['confidence'],
                    'log_id': log.id,
                    'timestamp': log.timestamp,
                    'subject': SubjectListSerializer(subject).data,
                    'is_wanted': is_wanted,
                    'warrant': warrant_data,
                    'offence_summary': offence_summary
                })
                
            # No match
            return Response({
                'match_found': False,
                'confidence': fr_result['confidence'],
                'log_id': log.id,
                'timestamp': log.timestamp,
                'message': 'No subject found in database.'
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IdentificationLogListView(generics.ListAPIView):
    """
    GET /api/identify/logs/
    """
    queryset = IdentificationLog.objects.select_related('officer', 'subject').order_by('-timestamp')
    serializer_class = IdentificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        
        if subject_id := params.get('subject_id'):
            qs = qs.filter(subject_id=subject_id)
        if officer_id := params.get('officer_id'):
            qs = qs.filter(officer_id=officer_id)
        if match := params.get('match_found'):
            qs = qs.filter(match_found=match.lower() == 'true')
            
        return qs
