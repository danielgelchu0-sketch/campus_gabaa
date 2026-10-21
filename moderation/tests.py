"""
Automated tests for moderation app:
Price discrepancy reporting by students, moderation dashboard access control,
and resolution workflows.
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from market.models import Category, Product, Shop, Listing
from .models import PriceReport

User = get_user_model()


class ModerationTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student1',
            email='student1@hu.edu.et',
            password='TestPassword123!',
            role=User.ROLE_STUDENT
        )
        self.vendor = User.objects.create_user(
            username='vendor1',
            email='vendor1@hu.edu.et',
            password='TestPassword123!',
            role=User.ROLE_SHOP_OWNER
        )
        self.moderator = User.objects.create_user(
            username='moderator1',
            email='moderator1@hu.edu.et',
            password='TestPassword123!',
            role=User.ROLE_MODERATOR,
            is_staff=True
        )

        self.category = Category.objects.create(name='Snacks', slug='snacks')
        self.product = Product.objects.create(
            category=self.category,
            name='Biscuits',
            slug='biscuits',
            unit='pack'
        )
        self.shop = Shop.objects.create(
            owner=self.vendor,
            name='Gate 1 Mart',
            slug='gate-1-mart',
            campus_zone='BATE_GATE',
            phone_number='0911223344',
            status=Shop.STATUS_APPROVED
        )
        self.listing = Listing.objects.create(
            shop=self.shop,
            product=self.product,
            price=Decimal('25.00')
        )

    def test_student_can_submit_price_report(self):
        """Verify student submits discrepancy report on a listing."""
        self.client.login(username='student1', password='TestPassword123!')
        report_url = reverse('moderation:report_listing', kwargs={'listing_id': self.listing.id})

        response = self.client.post(report_url, {
            'report_type': PriceReport.TYPE_WRONG_PRICE,
            'observed_price': '35.00',
            'comment': 'Shopkeeper charged 35 ETB instead of 25 ETB listed on the platform.',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(PriceReport.objects.filter(listing=self.listing).exists())
        report = PriceReport.objects.get(listing=self.listing)
        self.assertEqual(report.reported_by, self.student)
        self.assertEqual(report.observed_price, Decimal('35.00'))
        self.assertEqual(report.status, PriceReport.STATUS_PENDING)

    def test_moderation_dashboard_requires_moderator(self):
        """Verify non-moderators cannot access the moderation queue."""
        dashboard_url = reverse('moderation:dashboard')

        # Student denied
        self.client.login(username='student1', password='TestPassword123!')
        res_student = self.client.get(dashboard_url)
        self.assertEqual(res_student.status_code, 302)  # Redirected to login / denied

        # Moderator allowed
        self.client.login(username='moderator1', password='TestPassword123!')
        res_mod = self.client.get(dashboard_url)
        self.assertEqual(res_mod.status_code, 200)
        self.assertContains(res_mod, 'Campus Moderation Queue')

    def test_moderator_can_resolve_report(self):
        """Verify report resolution and status update."""
        report = PriceReport.objects.create(
            listing=self.listing,
            reported_by=self.student,
            report_type=PriceReport.TYPE_WRONG_PRICE,
            observed_price=Decimal('30.00'),
            comment='Discrepancy at kiosk',
            status=PriceReport.STATUS_PENDING
        )

        self.client.login(username='moderator1', password='TestPassword123!')
        resolve_url = reverse('moderation:report_detail', kwargs={'pk': report.id})

        response = self.client.post(resolve_url, {
            'action': 'resolve',
            'resolution_note': 'Contacted kiosk owner; owner updated shelf price to 30 ETB.',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        report.refresh_from_db()
        self.assertEqual(report.status, PriceReport.STATUS_RESOLVED)
        self.assertEqual(report.reviewed_by, self.moderator)
        self.assertIsNotNone(report.resolved_at)
