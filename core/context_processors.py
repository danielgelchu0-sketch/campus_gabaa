"""
Global context processors for Campus Gabaa.
Provides shared campus context, categories, and settings across all templates.
"""
from django.conf import settings

def global_campus_context(request):
    """
    Exposes commonly needed campus metadata across all templates without
    requiring manual query passing in every view.
    """
    # Import inside function to avoid circular imports during app initialization
    from market.models import Category, Shop

    try:
        categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    except Exception:
        # Fallback during initial migrations or database setup
        categories = []

    return {
        'NAV_CATEGORIES': categories,
        'PRICE_STALE_DAYS': getattr(settings, 'PRICE_STALE_DAYS', 7),
        'CAMPUS_NAME': 'Haramaya University',
        'CAMPUS_LOCATIONS': getattr(Shop, 'CAMPUS_ZONE_CHOICES', []),
    }
