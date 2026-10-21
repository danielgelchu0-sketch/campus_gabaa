"""
Forms for market app.
Supports Shop creation, Listing management with price tracking,
Product catalog requests, and advanced search/filtering.
"""

from decimal import Decimal
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Shop, Listing, Product, Category


class ShopForm(forms.ModelForm):
    """
    Shop profile creation and editing form.
    """
    class Meta:
        model = Shop
        fields = [
            'name',
            'campus_zone',
            'specific_location',
            'phone_number',
            'alternative_phone',
            'opening_hours',
            'description',
            'image',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g. Bate Aman Stationery & Copy')}),
            'campus_zone': forms.Select(attrs={'class': 'form-select'}),
            'specific_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g. Opposite Haramaya Post Office or Near Gate 1')
            }),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0912345678'}),
            'alternative_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Optional')}),
            'opening_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8:00 AM - 8:30 PM'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': _('Describe what your shop sells, services offered, etc.')
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ListingForm(forms.ModelForm):
    """
    Listing form used by shop owners to set price and availability.
    """
    class Meta:
        model = Listing
        fields = [
            'product',
            'price',
            'is_in_stock',
            'stock_notes',
        ]
        widgets = {
            'product': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.50',
                'min': '0.01',
                'placeholder': _('Price in ETB')
            }),
            'is_in_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stock_notes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g., Blue and Black available, 100 pages')
            }),
        }

    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop', None)
        super().__init__(*args, **kwargs)
        # Only active canonical products
        self.fields['product'].queryset = Product.objects.filter(is_active=True).select_related('category')
        if self.instance.pk:
            # Editing an existing listing; product shouldn't be switched
            self.fields['product'].disabled = True

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= Decimal('0.00'):
            raise forms.ValidationError(_('Price must be greater than zero Ethiopian Birr.'))
        if price > Decimal('100000.00'):
            raise forms.ValidationError(_('Price exceeds allowable campus marketplace threshold.'))
        return price


class ProductForm(forms.ModelForm):
    """
    Product creation form for vendors/moderators to submit new items to the catalog.
    """
    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'name_om',
            'name_am',
            'brand_or_model',
            'unit',
            'description',
            'image',
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Product name in English')}),
            'name_om': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Afaan Oromo name (optional)')}),
            'name_am': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Amharic name (optional)')}),
            'brand_or_model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('e.g. Deli, Bic, Pilot')}),
            'unit': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class SearchFilterForm(forms.Form):
    """
    Search and filter form for student product discovery.
    """
    SORT_CHOICES = [
        ('price_asc', _('Price: Lowest First')),
        ('price_desc', _('Price: Highest First')),
        ('name_asc', _('Name: A to Z')),
        ('updated_desc', _('Recently Updated')),
    ]

    q = forms.CharField(
        required=False,
        label=_('Search'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search stationery, electronics, snacks, books...')
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label=_('All Categories'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    campus_zone = forms.ChoiceField(
        choices=[('', _('All Campus Zones'))] + list(Shop.CAMPUS_ZONE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    in_stock_only = forms.BooleanField(
        required=False,
        initial=False,
        label=_('In Stock Only'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    fresh_only = forms.BooleanField(
        required=False,
        initial=False,
        label=_('Fresh Prices Only (< 7 days)'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='price_asc',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
