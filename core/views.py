"""
Views for core app.
Homepage, about, FAQ, health check endpoint for cloud monitoring.
"""

from datetime import timedelta
from django.db.models import Count, Min, Max, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from market.models import Product, Shop, Listing, Category, PriceHistory


def home(request):
    """
    Campus Gabaa landing page:
    - Search quick launcher
    - Live campus statistics (products, shops, recent updates)
    - Featured/Popular student products with lowest price
    - Category quick navigation
    - Stale price explainer
    """
    total_products = Product.objects.filter(is_active=True).count()
    total_shops = Shop.objects.filter(status=Shop.STATUS_APPROVED).count()
    
    # Active price updates in past 7 days
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_price_updates = PriceHistory.objects.filter(created_at__gte=seven_days_ago).count()
    
    # Categories with product counts
    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('products', filter=Q(products__is_active=True))
    ).order_by('order')[:8]

    # Featured products (products with multiple shop listings, great for comparison demonstration)
    featured_products = (
        Product.objects.filter(is_active=True)
        .annotate(
            listing_count=Count('listings', filter=Q(listings__shop__status=Shop.STATUS_APPROVED)),
            min_price=Min('listings__price', filter=Q(listings__shop__status=Shop.STATUS_APPROVED))
        )
        .filter(listing_count__gt=0)
        .select_related('category')
        .order_by('-listing_count')[:8]
    )

    context = {
        'total_products': total_products,
        'total_shops': total_shops,
        'recent_price_updates': recent_price_updates,
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """
    Academic capstone context, project motivation at Haramaya University,
    field methodology, and problem-solution architecture.
    """
    return render(request, 'core/about.html')


def faq(request):
    """
    Frequently Asked Questions for students, faculty, and local kiosk owners.
    """
    return render(request, 'core/faq.html')


def health_check(request):
    """
    Public health check endpoint for cloud hosting liveness & uptime probes
    (e.g., Render, Koyeb, UptimeRobot).
    """
    status_data = {
        'status': 'healthy',
        'service': 'Campus Gabaa (GabaaHU)',
        'target_institution': 'Haramaya University',
        'database': 'connected',
    }
    try:
        # Quick db ping
        Category.objects.exists()
    except Exception as e:
        status_data['status'] = 'unhealthy'
        status_data['database'] = str(e)
        return JsonResponse(status_data, status=503)

    return JsonResponse(status_data, status=200)
