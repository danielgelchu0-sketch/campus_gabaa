"""
URLs for core app.
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('how-to-use/', views.how_to_use, name='how_to_use'),
    path('about/', views.how_to_use, name='about'),
    path('faq/', views.faq, name='faq'),
    path('healthz/', views.health_check, name='health_check'),
    path('sw.js', views.service_worker, name='service_worker'),
    path('manifest.json', views.manifest, name='manifest'),
]
