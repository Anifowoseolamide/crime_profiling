from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Officer, PoliceStation


@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'division', 'lga', 'phone']
    search_fields = ['name', 'division', 'lga']
    ordering = ['name']


@admin.register(Officer)
class OfficerAdmin(UserAdmin):
    list_display = ['badge_number', 'get_full_name', 'rank', 'role', 'station', 'is_active']
    list_filter = ['role', 'station', 'is_active']
    search_fields = ['badge_number', 'first_name', 'last_name', 'rank']
    ordering = ['badge_number']

    fieldsets = (
        (None, {'fields': ('badge_number', 'password')}),
        ('Personal', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Role & Assignment', {'fields': ('rank', 'role', 'station')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('badge_number', 'first_name', 'last_name', 'rank', 'role', 'station', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['last_login', 'created_at']
