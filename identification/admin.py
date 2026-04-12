from django.contrib import admin
from .models import IdentificationLog

@admin.register(IdentificationLog)
class IdentificationLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'officer', 'subject', 'match_found', 'confidence_score', 'location']
    list_filter = ['match_found', 'timestamp']
    search_fields = ['officer__badge_number', 'subject__first_name', 'subject__last_name', 'location']
    readonly_fields = [
        'id', 'officer', 'subject', 'field_image_url', 
        'match_found', 'confidence_score', 'face_recognition_response',
        'location', 'latitude', 'longitude', 'notes', 'device_id', 'timestamp'
    ]
    
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
