from rest_framework import serializers
from .models import Offence
from subjects.serializers import SubjectListSerializer
from authentication.serializers import OfficerMiniSerializer, PoliceStationSerializer

class OffenceListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views."""
    subject_name = serializers.CharField(source='subject.get_full_name', read_only=True)
    arresting_officer_name = serializers.CharField(source='arresting_officer.get_full_name', read_only=True, allow_null=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    
    class Meta:
        model = Offence
        fields = [
            'id', 'offence_code', 'subject_name', 'offence_category', 'offence_title',
            'severity', 'status', 'incident_date', 'location', 
            'arresting_officer_name', 'station_name'
        ]

class OffenceDetailSerializer(serializers.ModelSerializer):
    """Full detail serializer."""
    subject = SubjectListSerializer(read_only=True)
    arresting_officer = OfficerMiniSerializer(read_only=True)
    station = PoliceStationSerializer(read_only=True)
    
    # Write only IDs for creation/update
    subject_id = serializers.UUIDField(write_only=True)
    arresting_officer_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    station_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Offence
        fields = [
            'id', 'offence_code', 'subject', 'subject_id',
            'offence_category', 'severity', 'status', 
            'offence_title', 'description', 
            'incident_date', 'reported_date', 
            'location', 'latitude', 'longitude',
            'arresting_officer', 'arresting_officer_id',
            'station', 'station_id',
            'evidence_images', 'court_case_number', 'penalty_issued', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'offence_code', 'reported_date', 'created_at', 'updated_at']
        
class OffenceUpdateStatusSerializer(serializers.ModelSerializer):
    """Restricted serializer for supervisors updating case status."""
    class Meta:
        model = Offence
        fields = ['status', 'court_case_number', 'penalty_issued', 'notes']
