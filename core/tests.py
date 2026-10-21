"""
Automated tests for core app:
Homepage, about, FAQ, health check endpoint, and i18n language switching.
"""

from django.test import TestCase
from django.urls import reverse
from market.models import Category, Product, Shop, Listing
from accounts.models import User


class CoreViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.user = User.objects.create_user(username='shopkeeper', role=User.ROLE_SHOP_OWNER)
        self.shop = Shop.objects.create(
            owner=self.user,
            name='Campus Tech',
            slug='campus-tech',
            campus_zone='MAIN_CAMPUS_KIOSK',
            phone_number='0911000000',
            status=Shop.STATUS_APPROVED
        )

    def test_homepage_renders_with_campus_context(self):
        """Verify home page loads successfully with campus branding and categories."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Campus Gabaa')
        self.assertContains(response, 'Haramaya University')
        self.assertContains(response, 'Electronics')

    def test_about_and_faq_pages(self):
        """Verify about page and FAQ render."""
        resp_about = self.client.get(reverse('core:about'))
        self.assertEqual(resp_about.status_code, 200)
        self.assertContains(resp_about, 'Academic Capstone')

        resp_faq = self.client.get(reverse('core:faq'))
        self.assertEqual(resp_faq.status_code, 200)
        self.assertContains(resp_faq, 'Frequently Asked Questions')

    def test_health_check_endpoint(self):
        """Verify cloud monitoring probe endpoint returns 200 healthy JSON."""
        response = self.client.get(reverse('core:health_check'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'Campus Gabaa (GabaaHU)')
        self.assertEqual(data['target_institution'], 'Haramaya University')

    def test_language_switcher_integration(self):
        """Verify language switcher endpoint sets active language cookie."""
        from django.conf import settings
        url = reverse('set_language')
        # Switch to Afaan Oromo
        response = self.client.post(url, {
            'language': 'om',
            'next': reverse('core:home')
        })
        self.assertEqual(response.status_code, 302)
        cookie_name = getattr(settings, 'LANGUAGE_COOKIE_NAME', 'django_language')
        self.assertIn(cookie_name, response.cookies)
        self.assertEqual(response.cookies[cookie_name].value, 'om')
