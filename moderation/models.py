"""
Moderation and crowd-sourced reporting models for Campus Gabaa.
Enables students to report stale prices, stock discrepancies, or closed kiosks,
providing a moderation queue for administrators and shop owners.
"""

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class PriceReport(models.Model):
    """
    User report flagging an inaccurate price, missing stock, or closed vendor.
    """
    TYPE_WRONG_PRICE = 'WRONG_PRICE'
    TYPE_OUT_OF_STOCK = 'OUT_OF_STOCK'
    TYPE_SHOP_CLOSED = 'SHOP_CLOSED'
    TYPE_MISLEADING = 'MISLEADING_INFO'
    TYPE_OTHER = 'OTHER'

    REPORT_TYPE_CHOICES = [
        (TYPE_WRONG_PRICE, _('Inaccurate / Higher Price at Shop')),
        (TYPE_OUT_OF_STOCK, _('Product is Out of Stock')),
        (TYPE_SHOP_CLOSED, _('Shop is Closed / Relocated')),
        (TYPE_MISLEADING, _('Misleading Description or Specification')),
        (TYPE_OTHER, _('Other Issue')),
    ]

    STATUS_PENDING = 'PENDING'
    STATUS_RESOLVED = 'RESOLVED'
    STATUS_DISMISSED = 'DISMISSED'

    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending Review')),
        (STATUS_RESOLVED, _('Resolved / Corrected')),
        (STATUS_DISMISSED, _('Dismissed / Inaccurate Report')),
    ]

    listing = models.ForeignKey(
        'market.Listing',
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name=_('Reported Listing')
    )
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submitted_reports',
        verbose_name=_('Reported By')
    )
    report_type = models.CharField(
        max_length=30,
        choices=REPORT_TYPE_CHOICES,
        default=TYPE_WRONG_PRICE,
        verbose_name=_('Report Type')
    )
    observed_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Actual Price Observed in Shop (ETB)'),
        help_text=_('If the price in store was different, enter what you saw.')
    )
    comment = models.TextField(
        verbose_name=_('Details & Description'),
        help_text=_('Describe what happened when you visited the shop.')
    )
    proof_image = models.ImageField(
        upload_to='report_proofs/',
        blank=True,
        null=True,
        verbose_name=_('Optional Receipt or Storefront Photo')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name=_('Resolution Status')
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_reports',
        verbose_name=_('Reviewed By Moderator')
    )
    resolution_note = models.TextField(
        blank=True,
        verbose_name=_('Moderator Resolution Note')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Price & Listing Report')
        verbose_name_plural = _('Price & Listing Reports')
        ordering = ['-created_at']

    def __str__(self):
        return f"Report #{self.id} on {self.listing} [{self.get_report_type_display()}]"

    def mark_resolved(self, moderator, note=''):
        self.status = self.STATUS_RESOLVED
        self.reviewed_by = moderator
        self.resolution_note = note
        self.resolved_at = timezone.now()
        self.save(update_fields=['status', 'reviewed_by', 'resolution_note', 'resolved_at'])

    def mark_dismissed(self, moderator, note=''):
        self.status = self.STATUS_DISMISSED
        self.reviewed_by = moderator
        self.resolution_note = note
        self.resolved_at = timezone.now()
        self.save(update_fields=['status', 'reviewed_by', 'resolution_note', 'resolved_at'])
