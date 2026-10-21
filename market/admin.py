"""
Django Admin registration for market app.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Category, Product, Shop, Listing, PriceHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_om', 'name_am', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'name_om', 'name_am')


class ListingInline(admin.TabularInline):
    model = Listing
    extra = 1
    fields = ('shop', 'price', 'is_in_stock', 'stock_notes', 'last_price_confirmed_at')
    readonly_fields = ('last_price_confirmed_at',)
    autocomplete_fields = ('shop',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand_or_model', 'unit', 'get_min_price', 'is_active', 'created_at')
    list_filter = ('category', 'unit', 'is_active')
    search_fields = ('name', 'name_om', 'name_am', 'brand_or_model', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ListingInline]

    @admin.display(description=_('Lowest Price (ETB)'))
    def get_min_price(self, obj):
        lowest = obj.lowest_price
        return f"{lowest} ETB" if lowest is not None else '-'


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'campus_zone', 'phone_number', 'status', 'is_verified', 'created_at')
    list_filter = ('campus_zone', 'status', 'is_verified')
    search_fields = ('name', 'owner__username', 'owner__email', 'phone_number', 'specific_location')
    prepopulated_fields = {'slug': ('name',)}
    actions = ['approve_shops', 'mark_verified']

    @admin.action(description=_('Approve selected shops'))
    def approve_shops(self, request, queryset):
        queryset.update(status=Shop.STATUS_APPROVED)

    @admin.action(description=_('Mark selected shops as physically verified'))
    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'shop',
        'price',
        'is_in_stock',
        'freshness_badge',
        'last_price_confirmed_at',
        'updated_at',
    )
    list_filter = ('is_in_stock', 'shop__campus_zone', 'created_at')
    search_fields = ('product__name', 'shop__name', 'stock_notes')
    autocomplete_fields = ('shop', 'product')
    actions = ['confirm_selected_prices', 'mark_in_stock', 'mark_out_of_stock']

    @admin.display(description=_('Freshness'))
    def freshness_badge(self, obj):
        status = obj.freshness_status
        return f"[{status}] ({obj.days_since_confirmed}d)"

    @admin.action(description=_('Re-confirm prices today for selected listings'))
    def confirm_selected_prices(self, request, queryset):
        for listing in queryset:
            listing.confirm_price(user=request.user)

    @admin.action(description=_('Mark selected listings as in stock'))
    def mark_in_stock(self, request, queryset):
        queryset.update(is_in_stock=True)

    @admin.action(description=_('Mark selected listings as out of stock'))
    def mark_out_of_stock(self, request, queryset):
        queryset.update(is_in_stock=False)


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('listing', 'old_price', 'new_price', 'changed_by', 'notes', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('listing__product__name', 'listing__shop__name', 'notes')
    readonly_fields = ('listing', 'old_price', 'new_price', 'changed_by', 'notes', 'created_at')
