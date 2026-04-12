from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'officer', 'action', 'target_type', 'target_id', 'ip_address']
    list_filter = ['action', 'target_type']
    search_fields = ['officer__badge_number', 'action', 'target_type']
    readonly_fields = ['id', 'officer', 'action', 'target_type', 'target_id', 'metadata', 'ip_address', 'timestamp']
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
