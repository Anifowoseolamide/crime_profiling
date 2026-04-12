from rest_framework import serializers
from .models import WantedPerson
from subjects.serializers import SubjectListSerializer
from authentication.serializers import OfficerMiniSerializer

class WantedPersonSerializer(serializers.ModelSerializer):
    subject = SubjectListSerializer(read_only=True)
    created_by = OfficerMiniSerializer(read_only=True)
    subject_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = WantedPerson
        fields = [
            'id', 'subject', 'subject_id', 'warrant_number', 
            'issuing_authority', 'reason', 'issued_date', 'expiry_date',
            'is_active', 'priority', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_warrant_number(self, value):
        # Allow same warrant number if we are updating the existing record
        qs = WantedPerson.objects.filter(warrant_number=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This warrant number already exists.")
        return value
