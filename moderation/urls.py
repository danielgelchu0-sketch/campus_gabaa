"""
URLs for moderation app.
"""

from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('report/listing/<int:listing_id>/', views.report_listing, name='report_listing'),
    path('dashboard/', views.moderation_dashboard, name='dashboard'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('shops/<int:pk>/approve/', views.approve_shop, name='approve_shop'),
]
