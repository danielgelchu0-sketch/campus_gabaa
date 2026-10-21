"""
Views for accounts app.
Handles authentication, registration, user profile, and role-based redirects.
"""

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from .forms import UserRegistrationForm, UserProfileForm
from .models import User


def register_view(request):
    """
    User registration for students and shop owners.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set active language to preferred language
            if user.preferred_language:
                translation.activate(user.preferred_language)

            login(request, user)
            messages.success(
                request,
                _('Welcome to Campus Gabaa, %(name)s! Your account has been created.') % {'name': user.first_name or user.username}
            )
            if user.is_shop_owner:
                messages.info(
                    request,
                    _('As a shop owner, you can now register your shop or kiosk profile to begin listing prices.')
                )
                return redirect('market:shop_create')
            return redirect('market:product_list')
        else:
            messages.error(request, _('Please correct the errors in the form.'))
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    User login view with validation and redirection.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Sync user's preferred language
            if user.preferred_language:
                translation.activate(user.preferred_language)

            messages.success(
                request,
                _('Logged in successfully. Welcome back, %(name)s!') % {'name': user.first_name or user.username}
            )
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('accounts:dashboard')
        else:
            messages.error(request, _('Invalid username or password. Please try again.'))
    else:
        form = AuthenticationForm(request)

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Logs out user and redirects to home with message.
    """
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return redirect('core:home')


@login_required
def profile_view(request):
    """
    View and edit current user profile details.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # Update active language if changed
            if user.preferred_language:
                translation.activate(user.preferred_language)

            messages.success(request, _('Your profile has been updated successfully.'))
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def dashboard_redirect(request):
    """
    Intelligent role-based dashboard router:
    - Shop Owners go to their shop management dashboard
    - Moderators go to the moderation queue
    - Students go to the campus product catalog
    """
    user = request.user
    if user.is_shop_owner:
        return redirect('market:shop_dashboard')
    elif user.is_moderator_user:
        return redirect('moderation:dashboard')
    else:
        return redirect('market:product_list')
