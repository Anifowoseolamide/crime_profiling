from django.contrib import admin
from .models import WantedPerson


@admin.register(WantedPerson)
class WantedPersonAdmin(admin.ModelAdmin):
    list_display = ['warrant_number', 'subject', 'priority', 'is_active', 'issued_date']
    list_filter = ['priority', 'is_active', 'issued_date']
    search_fields = ['warrant_number', 'subject__first_name', 'subject__last_name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['subject', 'created_by']
