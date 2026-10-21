"""
Automated tests for accounts app:
User registration, role-based authorization, permissions, and profile handling.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AccountsTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username='student1',
            email='student1@hu.edu.et',
            password='TestPassword123!',
            role=User.ROLE_STUDENT,
            phone_number='0911000001'
        )
        self.vendor = User.objects.create_user(
            username='vendor1',
            email='vendor1@hu.edu.et',
            password='TestPassword123!',
            role=User.ROLE_SHOP_OWNER,
            phone_number='0911000002'
        )
        self.moderator = User.objects.create_user(
            username='mod1',
            email='mod1@hu.edu.et',
            password='TestPassword123!',
            role=User.ROLE_MODERATOR,
            is_staff=True,
            phone_number='0911000003'
        )

    def test_user_roles_and_properties(self):
        """Verify role properties on custom User model."""
        self.assertTrue(self.student.is_student)
        self.assertFalse(self.student.is_shop_owner)
        self.assertFalse(self.student.is_moderator_user)

        self.assertFalse(self.vendor.is_student)
        self.assertTrue(self.vendor.is_shop_owner)
        self.assertFalse(self.vendor.is_moderator_user)

        self.assertTrue(self.moderator.is_moderator_user)

    def test_user_registration_student(self):
        """Test student account registration workflow."""
        url = reverse('accounts:register')
        data = {
            'username': 'newstudent',
            'first_name': 'Abebe',
            'last_name': 'Bikila',
            'email': 'abebe@student.hu.edu.et',
            'phone_number': '0912345678',
            'role': User.ROLE_STUDENT,
            'campus_id_or_dorm': 'Block 42, Room 10',
            'preferred_language': 'en',
            'password1': 'StrongPass2026!',
            'password2': 'StrongPass2026!',
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newstudent').exists())
        user = User.objects.get(username='newstudent')
        self.assertEqual(user.role, User.ROLE_STUDENT)

    def test_user_registration_duplicate_email(self):
        """Ensure duplicate emails are rejected."""
        url = reverse('accounts:register')
        data = {
            'username': 'unique_user',
            'first_name': 'Duplicate',
            'last_name': 'Tester',
            'email': 'student1@hu.edu.et',  # already taken by self.student
            'phone_number': '0999999999',
            'role': User.ROLE_STUDENT,
            'password1': 'StrongPass2026!',
            'password2': 'StrongPass2026!',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context['form'], 'email', 'An account with this email already exists.')

    def test_login_logout_workflow(self):
        """Test standard login and logout redirects."""
        login_url = reverse('accounts:login')
        response = self.client.post(login_url, {
            'username': 'student1',
            'password': 'TestPassword123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('_auth_user_id' in self.client.session)

        logout_url = reverse('accounts:logout')
        response = self.client.post(logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_profile_update(self):
        """Test authenticated user updating profile details."""
        self.client.login(username='student1', password='TestPassword123!')
        url = reverse('accounts:profile')
        response = self.client.post(url, {
            'first_name': 'Solomon',
            'last_name': 'Kebede',
            'email': 'solomon.new@hu.edu.et',
            'phone_number': '0988776655',
            'campus_id_or_dorm': 'Block 50',
            'preferred_language': 'om',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Solomon')
        self.assertEqual(self.student.preferred_language, 'om')
