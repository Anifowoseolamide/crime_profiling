from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'officer', 'action', 'target_type', 'gps_location', 'ip_address']
    list_filter = ['action', 'target_type']
    search_fields = ['officer__badge_number', 'action', 'target_type']
    readonly_fields = ['id', 'officer', 'action', 'target_type', 'target_id', 'metadata', 'ip_address', 'timestamp']
    ordering = ['-timestamp']

    def gps_location(self, obj):
        lat = obj.metadata.get('latitude')
        lng = obj.metadata.get('longitude')
        if lat and lng:
            from django.utils.html import format_html
            return format_html(
                '<a href="https://www.google.com/maps?q={},{} " target="_blank">📍 {}, {}</a>',
                lat, lng, round(lat, 4), round(lng, 4)
            )
        return "—"
    gps_location.short_description = 'GPS Location'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
