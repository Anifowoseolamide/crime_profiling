from rest_framework import serializers
from authentication.serializers import OfficerMiniSerializer
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    officer = OfficerMiniSerializer(read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'officer', 'action', 'target_type', 'target_id',
            'metadata', 'ip_address', 'timestamp',
        ]
        read_only_fields = fields
