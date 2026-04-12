from rest_framework import serializers
from .models import Subject, Mugshot
from authentication.serializers import OfficerMiniSerializer

class MugshotSerializer(serializers.ModelSerializer):
    captured_by = OfficerMiniSerializer(read_only=True)
    
    class Meta:
        model = Mugshot
        fields = [
            'id', 'image_url', 'is_primary', 'capture_date', 
            'captured_by', 'enrolled_in_face_recognition'
        ]
        read_only_fields = ['id', 'capture_date', 'enrolled_in_face_recognition']

class SubjectListSerializer(serializers.ModelSerializer):
    mugshotUrl = serializers.SerializerMethodField()
    location = serializers.CharField(source='last_known_location', read_only=True)
    lastSeen = serializers.DateTimeField(source='last_seen_date', read_only=True)
    coordinates = serializers.SerializerMethodField()
    offence_count = serializers.IntegerField(read_only=True, required=False)
    
    class Meta:
        model = Subject
        fields = [
            'id', 'first_name', 'last_name', 'aliases', 
            'risk_level', 'status', 'is_armed_dangerous', 
            'mugshotUrl', 'offence_count',
            'location', 'lastSeen', 'coordinates'
        ]
        
    def get_mugshotUrl(self, obj):
        return obj.primary_mugshot

    def get_coordinates(self, obj):
        if obj.last_known_lat is not None and obj.last_known_lng is not None:
            return {'lat': obj.last_known_lat, 'lng': obj.last_known_lng}
        return None

class SubjectDetailSerializer(serializers.ModelSerializer):
    mugshots = MugshotSerializer(many=True, read_only=True)
    mugshotUrl = serializers.SerializerMethodField()
    location = serializers.CharField(source='last_known_location', read_only=True)
    lastSeen = serializers.DateTimeField(source='last_seen_date', read_only=True)
    coordinates = serializers.SerializerMethodField()
    # offences and identification_logs injected via view context/query if needed
    
    class Meta:
        model = Subject
        fields = [
            'id', 'first_name', 'last_name', 'aliases', 'date_of_birth', 'gender',
            'nationality', 'state_of_origin', 'lga_of_origin', 'address', 'phone_numbers',
            'identifying_marks', 'risk_level', 'status', 'is_armed_dangerous',
            'face_recognition_id', 'created_at', 'updated_at',
            'mugshotUrl', 'mugshots',
            'location', 'lastSeen', 'coordinates'
        ]
        read_only_fields = ['id', 'face_recognition_id', 'created_at', 'updated_at']
        
    def get_mugshotUrl(self, obj):
        return obj.primary_mugshot

    def get_coordinates(self, obj):
        if obj.last_known_lat is not None and obj.last_known_lng is not None:
            return {'lat': obj.last_known_lat, 'lng': obj.last_known_lng}
        return None
