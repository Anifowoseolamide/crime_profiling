from django.contrib import admin
from .models import Subject, Mugshot

class MugshotInline(admin.TabularInline):
    model = Mugshot
    extra = 0
    fields = ['image_url', 'is_primary', 'enrolled_in_face_recognition', 'capture_date', 'captured_by']
    readonly_fields = ['capture_date']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'risk_level', 'status', 'is_armed_dangerous', 'last_known_location', 'last_seen_date']
    list_filter = ['risk_level', 'status', 'is_armed_dangerous', 'gender']
    search_fields = ['first_name', 'last_name', 'aliases', 'face_recognition_id']
    readonly_fields = ['face_recognition_id', 'created_at', 'updated_at']
    inlines = [MugshotInline]

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'aliases', 'status', 'risk_level', 'is_armed_dangerous')
        }),
        ('Biometrics & Profile', {
            'fields': ('date_of_birth', 'gender', 'nationality', 'state_of_origin', 'lga_of_origin', 'address', 'phone_numbers', 'identifying_marks')
        }),
        ('Geographic Tracking', {
            'fields': ('last_known_location', 'last_known_lat', 'last_known_lng', 'last_seen_date')
        }),
        ('System Metadata', {
            'fields': ('face_recognition_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Mugshot)
class MugshotAdmin(admin.ModelAdmin):
    list_display = ['subject', 'is_primary', 'enrolled_in_face_recognition', 'capture_date']
    list_filter = ['is_primary', 'enrolled_in_face_recognition']
    search_fields = ['subject__first_name', 'subject__last_name']
    readonly_fields = ['capture_date']
