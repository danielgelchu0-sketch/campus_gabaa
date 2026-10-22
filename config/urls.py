"""
URL configuration for Campus Gabaa (GabaaHU).
"""

import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import Http404
from django.urls import path, include

# Obscure, untraceable admin path to neutralize automated crawlers and university scanners
ADMIN_PATH = os.getenv('ADMIN_URL_PATH', 'gabaa-control-desk-hu26/').strip('/') + '/'


def fake_admin_trap(request):
    """Return 404 for automated bots scanning default /admin/"""
    raise Http404("Not Found")


urlpatterns = [
    path(ADMIN_PATH, admin.site.urls),
    path('admin/', fake_admin_trap),
    path('i18n/', include('django.conf.urls.i18n')),  # Django language switcher
    path('', include('core.urls', namespace='core')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('market/', include('market.urls', namespace='market')),
    path('moderation/', include('moderation.urls', namespace='moderation')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
