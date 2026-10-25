"""
Views for core app.
Homepage, about, FAQ, health check endpoint for cloud monitoring.
"""

from datetime import timedelta
import os
from django.conf import settings
from django.db.models import Count, Min, Max, Q
from django.http import JsonResponse, HttpResponse
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


def how_to_use(request):
    """
    Market-ready guide for students, buyers, and campus kiosk operators.
    Provides visual instructions on searching, comparing prices, checking freshness,
    and vendor onboarding within the Haramaya University perimeter.
    """
    return render(request, 'core/how_to_use.html')


def about(request):
    """
    Redirects or renders the modern how-to-use guide.
    """
    return render(request, 'core/how_to_use.html')


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


def service_worker(request):
    """
    Serves the root-scoped service worker for PWA offline caching & standalone installability.
    """
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'sw.js')
    try:
        with open(sw_path, 'r', encoding='utf-8') as f:
            content = f.read()
        response = HttpResponse(content, content_type='application/javascript')
        response['Service-Worker-Allowed'] = '/'
        response['Cache-Control'] = 'no-cache, must-revalidate'
        return response
    except FileNotFoundError:
        return HttpResponse("// SW not found", content_type='application/javascript', status=404)


def manifest(request):
    """
    Serves the PWA Web App Manifest at root domain with the standard MIME type.
    """
    manifest_path = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
        response = HttpResponse(content, content_type='application/manifest+json')
        response['Cache-Control'] = 'public, max-age=3600'
        return response
    except FileNotFoundError:
        return HttpResponse("{}", content_type='application/manifest+json', status=404)
