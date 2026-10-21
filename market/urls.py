"""
URLs for market app.
"""

from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    # Catalog and Discovery
    path('products/', views.product_list, name='product_list'),
    path('products/new/', views.product_create, name='product_create'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),

    # Campus Shops Directory
    path('shops/', views.shop_list, name='shop_list'),
    path('shops/register/', views.shop_create, name='shop_create'),
    path('shops/<slug:slug>/', views.shop_detail, name='shop_detail'),
    path('shops/<slug:slug>/edit/', views.shop_edit, name='shop_edit'),

    # Shop Owner Dashboard & Inventory Actions
    path('dashboard/', views.shop_dashboard, name='shop_dashboard'),
    path('shops/<slug:shop_slug>/listings/new/', views.listing_create, name='listing_create'),
    path('listings/<int:pk>/edit/', views.listing_edit, name='listing_edit'),
    path('listings/<int:pk>/confirm-price/', views.listing_confirm_price, name='listing_confirm_price'),
    path('listings/<int:pk>/toggle-stock/', views.listing_toggle_stock, name='listing_toggle_stock'),
]
