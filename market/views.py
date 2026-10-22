"""
Views for market app.
Comprehensive product discovery, multi-shop price comparison,
shop inventory management, and price freshness confirmation.
"""

from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Min, Max, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .forms import ShopForm, ListingForm, ProductForm, SearchFilterForm
from .models import Category, CampusZone, Product, Shop, Listing, PriceHistory


def product_list(request):
    """
    Core campus product discovery and search engine.
    Supports multi-criteria filtering: search keywords, category, campus zone,
    stock status, price freshness, and sorting.
    """
    form = SearchFilterForm(request.GET)
    products_qs = Product.objects.filter(is_active=True).select_related('category')

    # Apply search filter
    q = request.GET.get('q', '').strip()
    if q:
        products_qs = products_qs.filter(
            Q(name__icontains=q) |
            Q(name_om__icontains=q) |
            Q(name_am__icontains=q) |
            Q(brand_or_model__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q)
        )

    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        products_qs = products_qs.filter(category_id=category_id)

    # Campus zone filter (filters products that have listings in the specified campus zone)
    campus_zone = request.GET.get('campus_zone')
    if campus_zone:
        products_qs = products_qs.filter(
            listings__shop__campus_zone=campus_zone,
            listings__shop__status=Shop.STATUS_APPROVED
        ).distinct()

    # In-stock filter
    in_stock_only = request.GET.get('in_stock_only') == 'on' or request.GET.get('in_stock_only') == 'True'
    if in_stock_only:
        products_qs = products_qs.filter(
            listings__is_in_stock=True,
            listings__shop__status=Shop.STATUS_APPROVED
        ).distinct()

    # Annotate price aggregation for sorting and display
    products_qs = products_qs.annotate(
        min_price=Min('listings__price', filter=Q(listings__shop__status=Shop.STATUS_APPROVED)),
        max_price=Max('listings__price', filter=Q(listings__shop__status=Shop.STATUS_APPROVED)),
        shop_count=Count('listings', filter=Q(listings__shop__status=Shop.STATUS_APPROVED), distinct=True)
    )

    # Fresh-only filter (at least one listing updated in last 7 days)
    fresh_only = request.GET.get('fresh_only') == 'on' or request.GET.get('fresh_only') == 'True'
    if fresh_only:
        from django.conf import settings
        threshold_days = getattr(settings, 'PRICE_STALE_DAYS', 7)
        stale_cutoff = timezone.now() - timezone.timedelta(days=threshold_days)
        products_qs = products_qs.filter(
            listings__last_price_confirmed_at__gte=stale_cutoff,
            listings__shop__status=Shop.STATUS_APPROVED
        ).distinct()

    # Sorting
    sort = request.GET.get('sort', 'price_asc')
    if sort == 'price_desc':
        products_qs = products_qs.order_by('-min_price', 'name')
    elif sort == 'name_asc':
        products_qs = products_qs.order_by('name')
    elif sort == 'updated_desc':
        products_qs = products_qs.order_by('-updated_at')
    else:  # default price_asc
        products_qs = products_qs.order_by('min_price', 'name')

    # Pagination: 12 products per page
    paginator = Paginator(products_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Categories for quick chips
    categories = Category.objects.filter(is_active=True)

    context = {
        'form': form,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'selected_zone': campus_zone,
        'query': q,
        'total_results': paginator.count,
    }
    return render(request, 'market/product_list.html', context)


def product_detail(request, slug):
    """
    Canonical product detail page with the core 1-to-N price comparison matrix.
    Ranks shops by lowest price, displays freshness status, in-stock badges,
    contact info, and historical price movements.
    """
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug, is_active=True)

    # Fetch all listings from approved shops, sorted by price (cheapest first)
    listings = (
        Listing.objects.filter(product=product, shop__status=Shop.STATUS_APPROVED)
        .select_related('shop')
        .order_by('price')
    )

    # Calculate statistics
    prices = [l.price for l in listings]
    min_price = min(prices) if prices else None
    max_price = max(prices) if prices else None
    savings = (max_price - min_price) if (min_price and max_price and len(prices) > 1) else None

    # Price history across listings for transparency
    price_histories = (
        PriceHistory.objects.filter(listing__product=product)
        .select_related('listing__shop', 'changed_by')
        .order_by('-created_at')[:10]
    )

    context = {
        'product': product,
        'listings': listings,
        'min_price': min_price,
        'max_price': max_price,
        'savings': savings,
        'price_histories': price_histories,
        'now': timezone.now(),
    }
    return render(request, 'market/product_detail.html', context)


def shop_list(request):
    """
    Directory of all verified shops and kiosks across Haramaya University and Bate.
    """
    campus_zone = request.GET.get('zone', '')
    q = request.GET.get('q', '').strip()

    shops = Shop.objects.filter(status=Shop.STATUS_APPROVED).annotate(
        listing_count=Count('listings', filter=Q(listings__is_in_stock=True))
    )

    if campus_zone:
        shops = shops.filter(campus_zone=campus_zone)

    if q:
        shops = shops.filter(
            Q(name__icontains=q) |
            Q(specific_location__icontains=q) |
            Q(description__icontains=q)
        )

    shops = shops.order_by('-is_verified', 'name')

    db_zones = list(CampusZone.objects.filter(is_active=True))
    if db_zones:
        campus_zones = [(z.code, z.localized_name) for z in db_zones]
    else:
        campus_zones = Shop.CAMPUS_ZONE_CHOICES

    context = {
        'shops': shops,
        'campus_zones': campus_zones,
        'selected_zone': campus_zone,
        'query': q,
    }
    return render(request, 'market/shop_list.html', context)


def shop_detail(request, slug):
    """
    Storefront view for a specific campus vendor showing contact info,
    location, hours, and complete inventory of offerings.
    """
    shop = get_object_or_404(Shop.objects.select_related('owner'), slug=slug)
    
    # Non-approved shops can only be viewed by their owner or a moderator
    if shop.status != Shop.STATUS_APPROVED:
        if not (request.user.is_authenticated and request.user.can_manage_shop(shop)):
            messages.warning(request, _('This shop is currently undergoing verification.'))
            return redirect('market:shop_list')

    listings = (
        Listing.objects.filter(shop=shop)
        .select_related('product', 'product__category')
        .order_by('product__category__name', 'product__name')
    )

    context = {
        'shop': shop,
        'listings': listings,
        'can_manage': request.user.is_authenticated and request.user.can_manage_shop(shop),
    }
    return render(request, 'market/shop_detail.html', context)


@login_required
def shop_dashboard(request):
    """
    Shop Owner Control Center:
    - Lists vendor's registered shop(s)
    - High-visibility warnings for stale price listings
    - One-click price re-confirmation
    - Quick stock toggles
    - Summary analytics
    """
    user_shops = Shop.objects.filter(owner=request.user)

    if not user_shops.exists():
        messages.info(request, _('You do not have a registered shop profile yet. Let us create one now!'))
        return redirect('market:shop_create')

    # Default to first shop or selected shop
    shop_id = request.GET.get('shop_id')
    if shop_id:
        active_shop = get_object_or_404(user_shops, id=shop_id)
    else:
        active_shop = user_shops.first()

    listings = (
        Listing.objects.filter(shop=active_shop)
        .select_related('product', 'product__category')
        .order_by('-updated_at')
    )

    # Metrics
    total_listings = listings.count()
    in_stock_count = listings.filter(is_in_stock=True).count()
    
    # Calculate stale listings count
    from django.conf import settings
    threshold = getattr(settings, 'PRICE_STALE_DAYS', 7)
    cutoff = timezone.now() - timezone.timedelta(days=threshold)
    stale_count = listings.filter(last_price_confirmed_at__lt=cutoff).count()

    context = {
        'user_shops': user_shops,
        'active_shop': active_shop,
        'listings': listings,
        'total_listings': total_listings,
        'in_stock_count': in_stock_count,
        'stale_count': stale_count,
        'threshold_days': threshold,
    }
    return render(request, 'market/shop_dashboard.html', context)


@login_required
def shop_create(request):
    """
    Vendor onboarding: Register a new campus shop profile.
    """
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            # Automatically approve for demo/capstone purposes; in strict prod would be PENDING
            shop.status = Shop.STATUS_APPROVED
            shop.save()

            # Ensure user role reflects shop owner status
            if not request.user.is_shop_owner:
                request.user.role = request.user.ROLE_SHOP_OWNER
                request.user.save(update_fields=['role'])

            messages.success(
                request,
                _('Your shop "%(name)s" has been successfully created! You can now add product listings.') % {'name': shop.name}
            )
            return redirect('market:shop_dashboard')
    else:
        form = ShopForm()

    return render(request, 'market/shop_form.html', {'form': form, 'title': _('Register a New Campus Shop')})


@login_required
def shop_edit(request, slug):
    """
    Edit shop location, contact details, operating hours, or photo.
    """
    shop = get_object_or_404(Shop, slug=slug)
    if not request.user.can_manage_shop(shop):
        messages.error(request, _('You are not authorized to edit this shop.'))
        return redirect('market:shop_detail', slug=slug)

    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            messages.success(request, _('Shop details updated successfully.'))
            return redirect('market:shop_detail', slug=shop.slug)
    else:
        form = ShopForm(instance=shop)

    return render(request, 'market/shop_form.html', {'form': form, 'shop': shop, 'title': _('Edit Shop Details')})


@login_required
def listing_create(request, shop_slug):
    """
    Add a product to shop inventory with specific price and stock note.
    """
    shop = get_object_or_404(Shop, slug=shop_slug)
    if not request.user.can_manage_shop(shop):
        messages.error(request, _('You are not authorized to manage inventory for this shop.'))
        return redirect('market:shop_dashboard')

    if request.method == 'POST':
        form = ListingForm(request.POST, shop=shop)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.shop = shop
            listing.last_price_confirmed_at = timezone.now()
            
            # Check for existing listing for same product
            if Listing.objects.filter(shop=shop, product=listing.product).exists():
                messages.warning(
                    request,
                    _('This product is already in your inventory. You can edit its price directly.')
                )
                return redirect('market:shop_dashboard')

            listing.save()

            # Record initial price in history
            PriceHistory.objects.create(
                listing=listing,
                old_price=None,
                new_price=listing.price,
                changed_by=request.user,
                notes='Initial product listing created'
            )

            messages.success(
                request,
                _('Product "%(product)s" added to %(shop)s at %(price)s ETB.') % {
                    'product': listing.product.name,
                    'shop': shop.name,
                    'price': listing.price,
                }
            )
            return redirect('market:shop_dashboard')
    else:
        # Pre-select product if passed via query parameter (e.g. from product catalog)
        initial = {}
        product_id = request.GET.get('product_id')
        if product_id:
            initial['product'] = product_id
        form = ListingForm(initial=initial, shop=shop)

    context = {
        'form': form,
        'shop': shop,
        'title': _('Add Product to Shop Inventory'),
    }
    return render(request, 'market/listing_form.html', context)


@login_required
def listing_edit(request, pk):
    """
    Update price, stock status, or variant notes for an existing listing.
    Automatically logs price adjustments to PriceHistory.
    """
    listing = get_object_or_404(Listing.objects.select_related('shop', 'product'), pk=pk)
    if not request.user.can_manage_shop(listing.shop):
        messages.error(request, _('You are not authorized to edit this listing.'))
        return redirect('market:shop_dashboard')

    old_price = listing.price

    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing, shop=listing.shop)
        if form.is_valid():
            updated_listing = form.save(commit=False)
            new_price = updated_listing.price

            # If price changed or owner re-saved, update confirmation timestamp
            updated_listing.last_price_confirmed_at = timezone.now()
            updated_listing.save()

            if new_price != old_price:
                PriceHistory.objects.create(
                    listing=updated_listing,
                    old_price=old_price,
                    new_price=new_price,
                    changed_by=request.user,
                    notes=f"Price updated from {old_price} to {new_price} ETB"
                )
                messages.success(
                    request,
                    _('Price for %(product)s updated to %(price)s ETB (Timestamp refreshed).') % {
                        'product': listing.product.name,
                        'price': new_price,
                    }
                )
            else:
                messages.success(request, _('Listing details updated successfully.'))

            return redirect('market:shop_dashboard')
    else:
        form = ListingForm(instance=listing, shop=listing.shop)

    context = {
        'form': form,
        'listing': listing,
        'shop': listing.shop,
        'title': _('Edit Listing: %(product)s') % {'product': listing.product.name},
    }
    return render(request, 'market/listing_form.html', context)


@login_required
def listing_confirm_price(request, pk):
    """
    One-click action for vendor to verify that an existing price is still accurate today.
    Refreshes the freshness badge without altering the price amount.
    """
    if request.method != 'POST':
        return redirect('market:shop_dashboard')

    listing = get_object_or_404(Listing.objects.select_related('shop', 'product'), pk=pk)
    if not request.user.can_manage_shop(listing.shop):
        messages.error(request, _('Unauthorized action.'))
        return redirect('market:shop_dashboard')

    listing.confirm_price(user=request.user)
    messages.success(
        request,
        _('Price confirmed fresh today for %(product)s (%(price)s ETB)!') % {
            'product': listing.product.name,
            'price': listing.price,
        }
    )
    return redirect('market:shop_dashboard')


@login_required
def listing_toggle_stock(request, pk):
    """
    One-click action for vendor to toggle stock availability (In Stock / Out of Stock).
    """
    if request.method != 'POST':
        return redirect('market:shop_dashboard')

    listing = get_object_or_404(Listing.objects.select_related('shop', 'product'), pk=pk)
    if not request.user.can_manage_shop(listing.shop):
        messages.error(request, _('Unauthorized action.'))
        return redirect('market:shop_dashboard')

    listing.is_in_stock = not listing.is_in_stock
    listing.save(update_fields=['is_in_stock', 'updated_at'])

    status_str = _('In Stock') if listing.is_in_stock else _('Out of Stock')
    messages.info(
        request,
        _('Stock status for %(product)s changed to: %(status)s') % {
            'product': listing.product.name,
            'status': status_str,
        }
    )
    return redirect('market:shop_dashboard')


@login_required
def product_create(request):
    """
    Suggest or add a canonical product to the shared campus catalog.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(
                request,
                _('Product "%(product)s" added to catalog! You can now add it to your shop inventory.') % {'product': product.name}
            )
            # If user has shops, offer to immediately list it
            user_shop = Shop.objects.filter(owner=request.user).first()
            if user_shop:
                return redirect(f"{reverse('market:listing_create', kwargs={'shop_slug': user_shop.slug})}?product_id={product.id}")
            return redirect('market:product_detail', slug=product.slug)
    else:
        form = ProductForm()

    return render(request, 'market/product_form.html', {'form': form, 'title': _('Suggest / Add New Product')})
