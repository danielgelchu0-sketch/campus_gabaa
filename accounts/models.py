"""
Accounts models for Campus Gabaa.
Custom User model with role-based authorization for Haramaya University community.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom user model supporting:
    - Campus Buyers / Students
    - Shop Owners / Vendors
    - Campus Administrators / Moderators
    """
    ROLE_STUDENT = 'STUDENT'
    ROLE_SHOP_OWNER = 'SHOP_OWNER'
    ROLE_MODERATOR = 'MODERATOR'

    ROLE_CHOICES = [
        (ROLE_STUDENT, _('Student / Campus Buyer')),
        (ROLE_SHOP_OWNER, _('Shop Owner / Vendor')),
        (ROLE_MODERATOR, _('Moderator / Campus Admin')),
    ]

    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('om', _('Afaan Oromoo')),
        ('am', _('አማርኛ')),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_STUDENT,
        verbose_name=_('Role'),
        help_text=_('Designates user capabilities and access rights across the platform.')
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Phone Number'),
        help_text=_('Contact phone for shop inquiries or order verification.')
    )
    campus_id_or_dorm = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Campus ID / Dorm or Location'),
        help_text=_('e.g., HU Student ID, Dorm Block, or Department.')
    )
    preferred_language = models.CharField(
        max_length=5,
        choices=LANGUAGE_CHOICES,
        default='en',
        verbose_name=_('Preferred Language')
    )
    is_verified_vendor = models.BooleanField(
        default=False,
        verbose_name=_('Verified Vendor'),
        help_text=_('Indicates whether vendor identity has been physically verified on campus.')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        full = self.get_full_name()
        if full:
            return f"{full} ({self.username}) - {self.get_role_display()}"
        return f"{self.username} - {self.get_role_display()}"

    @property
    def is_student(self):
        return self.role == self.ROLE_STUDENT

    @property
    def is_shop_owner(self):
        return self.role == self.ROLE_SHOP_OWNER

    @property
    def is_moderator_user(self):
        return self.role == self.ROLE_MODERATOR or self.is_staff or self.is_superuser

    def can_manage_shop(self, shop):
        """
        Authorization check: shop owner or campus moderator/admin can manage the shop.
        """
        if not self.is_authenticated:
            return False
        if self.is_moderator_user:
            return True
        return shop.owner_id == self.id
