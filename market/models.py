"""
Market models for Campus Gabaa.
Implements the relational core: Categories, Canonical Products, Shops,
Shop-Specific Listings with price freshness logic, and Price History logs.
"""

from decimal import Decimal
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import get_language, gettext_lazy as _


class Category(models.Model):
    """
    Product categories tailored to Haramaya University student needs:
    Stationery, Electronics, Personal Care, Snacks, Printing/Services, etc.
    """
    name = models.CharField(max_length=120, unique=True, verbose_name=_('Category Name (English)'))
    name_om = models.CharField(max_length=120, blank=True, verbose_name=_('Category Name (Afaan Oromo)'))
    name_am = models.CharField(max_length=120, blank=True, verbose_name=_('Category Name (Amharic)'))
    slug = models.SlugField(max_length=140, unique=True)
    icon = models.CharField(
        max_length=50,
        default='bi-tag',
        verbose_name=_('Bootstrap/SVG Icon Identifier'),
        help_text=_('Bootstrap icon class name, e.g. bi-book, bi-laptop, bi-basket, bi-cup-hot')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Display Order'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'name']

    def __str__(self):
        return self.localized_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def localized_name(self):
        """
        Dynamically returns the category name in the active session language.
        """
        lang = get_language() or 'en'
        if lang.startswith('om') and self.name_om:
            return self.name_om
        elif lang.startswith('am') and self.name_am:
            return self.name_am
        return self.name


class Product(models.Model):
    """
    Canonical Product catalog entry.
    Decoupled from individual shops to enable 1-to-N shop price comparison.
    """
    UNIT_CHOICES = [
        ('piece', _('Piece / Item')),
        ('pack', _('Pack / Bundle')),
        ('box', _('Box / Carton')),
        ('kg', _('Kilogram (kg)')),
        ('liter', _('Liter (L)')),
        ('page', _('Page (Printing)')),
        ('set', _('Set')),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_('Category')
    )
    name = models.CharField(max_length=200, db_index=True, verbose_name=_('Product Name (English)'))
    name_om = models.CharField(max_length=200, blank=True, verbose_name=_('Product Name (Afaan Oromo)'))
    name_am = models.CharField(max_length=200, blank=True, verbose_name=_('Product Name (Amharic)'))
    slug = models.SlugField(max_length=240, unique=True)
    brand_or_model = models.CharField(
        max_length=120,
        blank=True,
        verbose_name=_('Brand or Model Specification'),
        help_text=_('e.g. Deli, Bic, HP, Samsung, Unbranded')
    )
    unit = models.CharField(
        max_length=30,
        choices=UNIT_CHOICES,
        default='piece',
        verbose_name=_('Unit of Measure')
    )
    description = models.TextField(blank=True, verbose_name=_('Product Description'))
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name=_('Product Image')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Active in Catalog'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category', 'is_active']),
        ]

    def __str__(self):
        return self.localized_name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            candidate = base_slug
            idx = 1
            while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{idx}"
                idx += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('market:product_detail', kwargs={'slug': self.slug})

    @property
    def localized_name(self):
        lang = get_language() or 'en'
        if lang.startswith('om') and self.name_om:
            return self.name_om
        elif lang.startswith('am') and self.name_am:
            return self.name_am
        return self.name

    def get_approved_listings(self):
        """
        Returns active listings from approved shops only.
        """
        return self.listings.filter(
            shop__status=Shop.STATUS_APPROVED
        ).select_related('shop').order_by('price')

    def get_price_range(self):
        """
        Returns a tuple: (min_price, max_price, listing_count, in_stock_count)
        """
        listings = self.get_approved_listings()
        if not listings.exists():
            return None, None, 0, 0
        prices = [l.price for l in listings]
        in_stock = listings.filter(is_in_stock=True).count()
        return min(prices), max(prices), len(prices), in_stock

    @property
    def lowest_price(self):
        min_p, _, _, _ = self.get_price_range()
        return min_p

    @property
    def highest_price(self):
        _, max_p, _, _ = self.get_price_range()
        return max_p

    @property
    def active_shop_count(self):
        _, _, count, _ = self.get_price_range()
        return count


class Shop(models.Model):
    """
    Physical shop, kiosk, bookstore, or service center in Haramaya & Bate.
    """
    CAMPUS_ZONE_CHOICES = [
        ('MAIN_CAMPUS_KIOSK', _('Haramaya Main Campus (Dorm / Admin Kiosks)')),
        ('BATE_GATE', _('Bate Gate / Campus Entrance')),
        ('BATE_MARKET', _('Bate Town Center & Market')),
        ('HARAMAYA_TOWN', _('Haramaya Town Commercial Area')),
        ('AGRICULTURE_CAMPUS', _('Agriculture & Veterinary Campus Zone')),
    ]

    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_SUSPENDED = 'SUSPENDED'

    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending Verification')),
        (STATUS_APPROVED, _('Approved & Active')),
        (STATUS_SUSPENDED, _('Suspended')),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shops',
        verbose_name=_('Shop Owner')
    )
    name = models.CharField(max_length=180, db_index=True, verbose_name=_('Shop Name'))
    slug = models.SlugField(max_length=200, unique=True)
    campus_zone = models.CharField(
        max_length=50,
        choices=CAMPUS_ZONE_CHOICES,
        default='BATE_GATE',
        verbose_name=_('Campus Location Zone')
    )
    specific_location = models.CharField(
        max_length=255,
        verbose_name=_('Detailed Physical Location / Landmark'),
        help_text=_('e.g. Opposite Dorm Block 42 Kiosk #4, or Behind Bate Grand Mosque')
    )
    phone_number = models.CharField(
        max_length=25,
        verbose_name=_('Primary Phone Number'),
        help_text=_('Ethiopian phone number, e.g. 0912345678')
    )
    alternative_phone = models.CharField(
        max_length=25,
        blank=True,
        verbose_name=_('Alternative Phone / Telegram')
    )
    opening_hours = models.CharField(
        max_length=120,
        default='8:00 AM - 8:30 PM',
        verbose_name=_('Opening Hours')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('About the Shop / Specialties')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_APPROVED,
        verbose_name=_('Verification Status')
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('Physically Verified Badge')
    )
    image = models.ImageField(
        upload_to='shops/',
        blank=True,
        null=True,
        verbose_name=_('Shop Storefront Photo')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Shop')
        verbose_name_plural = _('Shops')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_campus_zone_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            candidate = base_slug
            idx = 1
            while Shop.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{idx}"
                idx += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('market:shop_detail', kwargs={'slug': self.slug})

    @property
    def is_active(self):
        return self.status == self.STATUS_APPROVED


class Listing(models.Model):
    """
    Shop-specific pricing and availability for a canonical product.
    Includes stale-price detection logic and confirmation timestamps.
    """
    FRESHNESS_FRESH = 'FRESH'
    FRESHNESS_EXPIRING = 'EXPIRING'
    FRESHNESS_STALE = 'STALE'

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name=_('Shop')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='listings',
        verbose_name=_('Product')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Price (ETB)'),
        help_text=_('Unit price in Ethiopian Birr')
    )
    is_in_stock = models.BooleanField(
        default=True,
        verbose_name=_('Currently In Stock')
    )
    stock_notes = models.CharField(
        max_length=150,
        blank=True,
        verbose_name=_('Stock or Variant Note'),
        help_text=_('e.g., A4 ruled, 50 sheets, Black/Blue only')
    )
    last_price_confirmed_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Price Last Confirmed At'),
        help_text=_('Timestamp when vendor explicitly verified this price')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Product Listing')
        verbose_name_plural = _('Product Listings')
        unique_together = ('shop', 'product')
        ordering = ['price']
        indexes = [
            models.Index(fields=['product', 'is_in_stock', 'price']),
            models.Index(fields=['shop', 'updated_at']),
        ]

    def __str__(self):
        return f"{self.product.name} @ {self.shop.name}: {self.price} ETB"

    @property
    def days_since_confirmed(self):
        delta = timezone.now() - self.last_price_confirmed_at
        return max(0, delta.days)

    @property
    def is_stale(self):
        threshold = getattr(settings, 'PRICE_STALE_DAYS', 7)
        return self.days_since_confirmed >= threshold

    @property
    def freshness_status(self):
        """
        Categorizes price confidence:
        - FRESH: Confirmed within 3 days
        - EXPIRING: Confirmed 3 to 7 days ago
        - STALE: Confirmed 7+ days ago (unverified)
        """
        days = self.days_since_confirmed
        threshold = getattr(settings, 'PRICE_STALE_DAYS', 7)
        if days < 3:
            return self.FRESHNESS_FRESH
        elif days < threshold:
            return self.FRESHNESS_EXPIRING
        return self.FRESHNESS_STALE

    def confirm_price(self, user=None):
        """
        Action to refresh confirmation timestamp when shop owner affirms current price.
        """
        now = timezone.now()
        self.last_price_confirmed_at = now
        self.save(update_fields=['last_price_confirmed_at', 'updated_at'])
        # Also log to history as a confirmation
        PriceHistory.objects.create(
            listing=self,
            old_price=self.price,
            new_price=self.price,
            changed_by=user,
            notes='Price re-confirmed by vendor'
        )


class PriceHistory(models.Model):
    """
    Immutable audit log tracking every price adjustment or confirmation.
    Vital for transparency and analyzing campus inflation trends.
    """
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name='price_history',
        verbose_name=_('Listing')
    )
    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Previous Price (ETB)')
    )
    new_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Updated Price (ETB)')
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Modified By')
    )
    notes = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Change Notes')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Price History Entry')
        verbose_name_plural = _('Price History Entries')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.listing.product.name} ({self.listing.shop.name}): {self.old_price} -> {self.new_price} ETB"
