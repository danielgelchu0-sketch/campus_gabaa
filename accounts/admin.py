"""
Django Admin registration for accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Enhanced User admin display showing campus roles, phone, and verification status.
    """
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'phone_number',
        'is_verified_vendor',
        'is_staff',
    )
    list_filter = ('role', 'is_verified_vendor', 'is_staff', 'is_active', 'preferred_language')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'campus_id_or_dorm')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        (_('Campus Gabaa Profile'), {
            'fields': (
                'role',
                'phone_number',
                'campus_id_or_dorm',
                'preferred_language',
                'is_verified_vendor',
            ),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Campus Gabaa Profile'), {
            'fields': (
                'role',
                'phone_number',
                'campus_id_or_dorm',
                'preferred_language',
            ),
        }),
    )
