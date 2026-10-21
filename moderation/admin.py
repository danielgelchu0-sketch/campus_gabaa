"""
Django Admin registration for moderation app.
"""

from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import PriceReport


@admin.register(PriceReport)
class PriceReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'listing',
        'reported_by',
        'report_type',
        'observed_price',
        'status',
        'created_at',
        'resolved_at',
    )
    list_filter = ('status', 'report_type', 'created_at')
    search_fields = (
        'listing__product__name',
        'listing__shop__name',
        'reported_by__username',
        'comment',
        'resolution_note',
    )
    readonly_fields = ('created_at', 'resolved_at')
    actions = ['mark_resolved', 'mark_dismissed']

    @admin.action(description=_('Mark selected reports as RESOLVED'))
    def mark_resolved(self, request, queryset):
        for report in queryset:
            report.mark_resolved(moderator=request.user, note='Resolved via batch admin action.')

    @admin.action(description=_('Mark selected reports as DISMISSED'))
    def mark_dismissed(self, request, queryset):
        for report in queryset:
            report.mark_dismissed(moderator=request.user, note='Dismissed via batch admin action.')
