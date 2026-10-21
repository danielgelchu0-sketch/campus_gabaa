"""
Views for moderation app.
Crowd-sourced reporting of price discrepancies, moderation queues,
and administrative approvals.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from market.models import Listing, Shop
from .forms import PriceReportForm, ModerationResolutionForm
from .models import PriceReport


def is_moderator(user):
    """
    Authorization helper: user is authenticated and is a moderator or staff.
    """
    return user.is_authenticated and (user.is_moderator_user or user.is_staff or user.is_superuser)


@login_required
def report_listing(request, listing_id):
    """
    Submits a price discrepancy, out-of-stock, or closed kiosk report.
    Available to all logged-in students and campus members.
    """
    listing = get_object_or_404(Listing.objects.select_related('shop', 'product'), pk=listing_id)

    if request.method == 'POST':
        form = PriceReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.listing = listing
            report.reported_by = request.user
            report.save()

            messages.success(
                request,
                _('Thank you! Your report on "%(product)s" at %(shop)s has been submitted for review.') % {
                    'product': listing.product.name,
                    'shop': listing.shop.name,
                }
            )
            return redirect('market:product_detail', slug=listing.product.slug)
    else:
        form = PriceReportForm()

    context = {
        'form': form,
        'listing': listing,
        'title': _('Report Listing Discrepancy'),
    }
    return render(request, 'moderation/report_form.html', context)


@login_required
@user_passes_test(is_moderator)
def moderation_dashboard(request):
    """
    Campus Moderator & Administrator Dashboard:
    - Lists pending community price/stock reports
    - Lists shops awaiting administrative verification
    - Key metrics on report volume and resolution rates
    """
    status_filter = request.GET.get('status', PriceReport.STATUS_PENDING)
    
    reports = PriceReport.objects.select_related(
        'listing__product',
        'listing__shop',
        'reported_by',
        'reviewed_by'
    )
    if status_filter != 'ALL':
        reports = reports.filter(status=status_filter)
    
    reports = reports.order_by('-created_at')

    # Pending shops
    pending_shops = Shop.objects.filter(status=Shop.STATUS_PENDING).select_related('owner')

    # Summary counts
    pending_reports_count = PriceReport.objects.filter(status=PriceReport.STATUS_PENDING).count()
    pending_shops_count = pending_shops.count()
    resolved_reports_count = PriceReport.objects.filter(status=PriceReport.STATUS_RESOLVED).count()

    context = {
        'reports': reports,
        'pending_shops': pending_shops,
        'pending_reports_count': pending_reports_count,
        'pending_shops_count': pending_shops_count,
        'resolved_reports_count': resolved_reports_count,
        'current_status': status_filter,
    }
    return render(request, 'moderation/dashboard.html', context)


@login_required
@user_passes_test(is_moderator)
def report_detail(request, pk):
    """
    Examine and resolve/dismiss an individual price report.
    """
    report = get_object_or_404(
        PriceReport.objects.select_related('listing__product', 'listing__shop', 'reported_by'),
        pk=pk
    )

    if request.method == 'POST':
        form = ModerationResolutionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            note = form.cleaned_data['resolution_note']
            if action == 'resolve':
                report.mark_resolved(moderator=request.user, note=note)
                messages.success(request, _('Report #%(id)s marked as RESOLVED.') % {'id': report.id})
            else:
                report.mark_dismissed(moderator=request.user, note=note)
                messages.info(request, _('Report #%(id)s has been DISMISSED.') % {'id': report.id})
            return redirect('moderation:dashboard')
    else:
        form = ModerationResolutionForm()

    context = {
        'report': report,
        'form': form,
    }
    return render(request, 'moderation/report_detail.html', context)


@login_required
@user_passes_test(is_moderator)
def approve_shop(request, pk):
    """
    Administrative approval of a pending shop.
    """
    if request.method != 'POST':
        return redirect('moderation:dashboard')

    shop = get_object_or_404(Shop, pk=pk)
    action = request.POST.get('action', 'approve')

    if action == 'approve':
        shop.status = Shop.STATUS_APPROVED
        shop.is_verified = True
        shop.save(update_fields=['status', 'is_verified', 'updated_at'])
        messages.success(request, _('Shop "%(name)s" has been approved and verified!') % {'name': shop.name})
    elif action == 'suspend':
        shop.status = Shop.STATUS_SUSPENDED
        shop.save(update_fields=['status', 'updated_at'])
        messages.warning(request, _('Shop "%(name)s" has been suspended.') % {'name': shop.name})

    return redirect('moderation:dashboard')
