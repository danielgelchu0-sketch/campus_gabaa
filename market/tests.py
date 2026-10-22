"""
Automated tests for market app:
Catalog modeling, 1-to-N multi-shop price comparison math,
price freshness calculation, ownership security, and search filters.
"""

from decimal import Decimal
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Category, Product, Shop, Listing, PriceHistory

User = get_user_model()


class MarketModelAndLogicTests(TestCase):
    def setUp(self):
        self.vendor1 = User.objects.create_user(
            username='vendor1',
            email='v1@hu.edu.et',
            password='TestPassword123!',
            role=User.ROLE_SHOP_OWNER
        )
        self.vendor2 = User.objects.create_user(
            username='vendor2',
            email='v2@hu.edu.et',
            password='TestPassword123!',
            role=User.ROLE_SHOP_OWNER
        )
        self.student = User.objects.create_user(
            username='student1',
            email='s1@hu.edu.et',
            password='TestPassword123!',
            role=User.ROLE_STUDENT
        )

        self.category = Category.objects.create(
            name='Stationery',
            name_om='Waraqaa',
            name_am='የጽሕፈት መሣሪያዎች',
            slug='stationery',
            icon='bi-book'
        )

        self.product = Product.objects.create(
            category=self.category,
            name='Deli Blue Pen',
            name_om='Qalama Cuquliisaa',
            name_am='ሰማያዊ እስክሪብቶ',
            slug='deli-blue-pen',
            unit='piece'
        )

        self.shop1 = Shop.objects.create(
            owner=self.vendor1,
            name='Aman Kiosk',
            slug='aman-kiosk',
            campus_zone='MAIN_CAMPUS_KIOSK',
            specific_location='Block 42',
            phone_number='0911223344',
            status=Shop.STATUS_APPROVED
        )

        self.shop2 = Shop.objects.create(
            owner=self.vendor2,
            name='Bate Gateway Mart',
            slug='bate-mart',
            campus_zone='BATE_GATE',
            specific_location='Bate Gate Entrance',
            phone_number='0922334455',
            status=Shop.STATUS_APPROVED
        )

    def test_multi_shop_price_comparison(self):
        """
        Verify that 1 canonical product aggregates listings from multiple shops
        and accurately identifies lowest price, highest price, and active shop count.
        """
        Listing.objects.create(
            shop=self.shop1,
            product=self.product,
            price=Decimal('35.00'),
            is_in_stock=True
        )
        Listing.objects.create(
            shop=self.shop2,
            product=self.product,
            price=Decimal('28.00'),
            is_in_stock=True
        )

        self.assertEqual(self.product.lowest_price, Decimal('28.00'))
        self.assertEqual(self.product.highest_price, Decimal('35.00'))
        self.assertEqual(self.product.active_shop_count, 2)

    def test_price_freshness_status_tiers(self):
        """
        Verify price freshness calculation:
        - FRESH: < 3 days
        - EXPIRING: 3 to 7 days
        - STALE: >= 7 days
        """
        now = timezone.now()

        # Listing 1: Confirmed today
        listing_fresh = Listing.objects.create(
            shop=self.shop1,
            product=self.product,
            price=Decimal('30.00'),
            last_price_confirmed_at=now - timedelta(hours=5)
        )
        self.assertEqual(listing_fresh.freshness_status, Listing.FRESHNESS_FRESH)
        self.assertFalse(listing_fresh.is_stale)

        # Listing 2: Confirmed 4 days ago
        listing_expiring = Listing(
            shop=self.shop2,
            product=self.product,
            price=Decimal('30.00'),
            last_price_confirmed_at=now - timedelta(days=4)
        )
        self.assertEqual(listing_expiring.freshness_status, Listing.FRESHNESS_EXPIRING)
        self.assertFalse(listing_expiring.is_stale)

        # Listing 3: Confirmed 10 days ago (Stale)
        listing_stale = Listing(
            shop=self.shop2,
            product=self.product,
            price=Decimal('30.00'),
            last_price_confirmed_at=now - timedelta(days=10)
        )
        self.assertEqual(listing_stale.freshness_status, Listing.FRESHNESS_STALE)
        self.assertTrue(listing_stale.is_stale)

    def test_one_click_price_confirmation(self):
        """Verify that vendor confirming price refreshes timestamp and writes audit history."""
        past_date = timezone.now() - timedelta(days=12)
        listing = Listing.objects.create(
            shop=self.shop1,
            product=self.product,
            price=Decimal('30.00'),
            last_price_confirmed_at=past_date
        )
        self.assertTrue(listing.is_stale)

        # Vendor confirms price today
        self.client.login(username='vendor1', password='TestPassword123!')
        url = reverse('market:listing_confirm_price', kwargs={'pk': listing.pk})
        response = self.client.post(url, follow=True)
        self.assertEqual(response.status_code, 200)

        listing.refresh_from_db()
        self.assertEqual(listing.freshness_status, Listing.FRESHNESS_FRESH)
        self.assertFalse(listing.is_stale)
        self.assertTrue(PriceHistory.objects.filter(listing=listing).exists())

    def test_one_click_stock_toggle(self):
        """Verify stock availability toggle."""
        listing = Listing.objects.create(
            shop=self.shop1,
            product=self.product,
            price=Decimal('30.00'),
            is_in_stock=True
        )

        self.client.login(username='vendor1', password='TestPassword123!')
        url = reverse('market:listing_toggle_stock', kwargs={'pk': listing.pk})
        self.client.post(url, follow=True)

        listing.refresh_from_db()
        self.assertFalse(listing.is_in_stock)

    def test_unauthorized_shop_management_blocked(self):
        """Ensure Vendor 2 cannot edit Vendor 1's shop or listing."""
        listing = Listing.objects.create(
            shop=self.shop1,
            product=self.product,
            price=Decimal('30.00')
        )

        # Login as Vendor 2
        self.client.login(username='vendor2', password='TestPassword123!')
        edit_url = reverse('market:listing_edit', kwargs={'pk': listing.pk})
        response = self.client.get(edit_url, follow=True)
        # Should be redirected away with error message
        self.assertContains(response, 'You are not authorized to edit this listing.')

    def test_search_and_category_filter(self):
        """Test search query and category filtering."""
        Listing.objects.create(
            shop=self.shop1,
            product=self.product,
            price=Decimal('30.00'),
            is_in_stock=True
        )

        list_url = reverse('market:product_list')

        # Matching search
        resp = self.client.get(list_url, {'q': 'Deli'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Deli Blue Pen')

        # Non-matching search
        resp_empty = self.client.get(list_url, {'q': 'NonExistentLaptopBrandXYZ'})
        self.assertEqual(resp_empty.status_code, 200)
        self.assertContains(resp_empty, 'No matching campus products found')

        # Category filter
        resp_cat = self.client.get(list_url, {'category': self.category.id})
        self.assertEqual(resp_cat.status_code, 200)
        self.assertContains(resp_cat, 'Deli Blue Pen')
