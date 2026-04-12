"""
AuditLogMixin — attach to any APIView or GenericAPIView to auto-write
an AuditLog entry after successful write operations (POST/PUT/PATCH).

Usage:
    class MyView(AuditLogMixin, generics.CreateAPIView):
        audit_action = 'SUBJECT_CREATED'
        audit_target_type = 'Subject'
"""
from audit.models import AuditLog


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


class AuditLogMixin:
    """
    Mixin for DRF views. Override audit_action and audit_target_type.
    Calls write_audit_log() after perform_create / perform_update.
    """
    audit_action = 'ACTION'
    audit_target_type = ''

    def write_audit_log(self, instance, action=None, extra_meta=None):
        officer = self.request.user if self.request.user.is_authenticated else None
        meta = extra_meta or {}
        AuditLog.log(
            officer=officer,
            action=action or self.audit_action,
            target_type=self.audit_target_type,
            target_id=getattr(instance, 'id', None),
            metadata=meta,
            ip_address=get_client_ip(self.request),
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        self.write_audit_log(instance)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        self.write_audit_log(instance, action=self.audit_action.replace('CREATED', 'UPDATED'))
        return instance
