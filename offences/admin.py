from django.contrib import admin
from .models import Offence

@admin.register(Offence)
class OffenceAdmin(admin.ModelAdmin):
    list_display = ['offence_code', 'subject', 'offence_category', 'severity', 'status', 'incident_date']
    list_filter = ['status', 'severity', 'offence_category', 'station']
    search_fields = ['offence_code', 'subject__first_name', 'subject__last_name', 'court_case_number']
    readonly_fields = ['offence_code', 'reported_date', 'created_at', 'updated_at']
    date_hierarchy = 'incident_date'
    
    fieldsets = (
        (None, {
            'fields': ('offence_code', 'subject', 'status')
        }),
        ('Classification', {
            'fields': ('offence_category', 'severity')
        }),
        ('Details', {
            'fields': ('offence_title', 'description', 'incident_date', 'reported_date')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude', 'station')
        }),
        ('Enforcement', {
            'fields': ('arresting_officer', 'evidence_images')
        }),
        ('Outcome', {
            'fields': ('court_case_number', 'penalty_issued', 'notes')
        }),
        ('System', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
