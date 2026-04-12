from rest_framework import serializers
from .models import IdentificationLog
from subjects.serializers import SubjectListSerializer
from authentication.serializers import OfficerMiniSerializer
from wanted.models import WantedPerson
from offences.models import Offence

class IdentificationLogSerializer(serializers.ModelSerializer):
    officer = OfficerMiniSerializer(read_only=True)
    subject = SubjectListSerializer(read_only=True)

    class Meta:
        model = IdentificationLog
        fields = [
            'id', 'officer', 'subject', 'field_image_url', 
            'match_found', 'confidence_score', 'location', 
            'latitude', 'longitude', 'notes', 'timestamp', 'device_id'
        ]
        read_only_fields = ['id', 'timestamp']

class IdentifyRequestSerializer(serializers.Serializer):
    """Payload sent by the frontend for a field scan."""
    image = serializers.CharField(required=True, help_text="Base64 encoded JPEG")
    location = serializers.CharField(required=False, allow_blank=True)
    latitude = serializers.FloatField(required=False, allow_null=True)
    longitude = serializers.FloatField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    device_id = serializers.CharField(required=False, allow_blank=True)
