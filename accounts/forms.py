"""
Forms for accounts app.
User registration and profile management with campus-specific fields.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Registration form supporting both student buyers and local shop owners.
    """
    first_name = forms.CharField(max_length=50, required=True, label=_('First Name'))
    last_name = forms.CharField(max_length=50, required=True, label=_('Father / Last Name'))
    email = forms.EmailField(required=True, label=_('Email Address'))
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        label=_('Phone Number'),
        help_text=_('e.g., 0912345678 or +251912345678')
    )
    role = forms.ChoiceField(
        choices=[
            (User.ROLE_STUDENT, _('Student / Campus Buyer')),
            (User.ROLE_SHOP_OWNER, _('Shop Owner / Vendor')),
        ],
        initial=User.ROLE_STUDENT,
        label=_('Account Type'),
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    campus_id_or_dorm = forms.CharField(
        max_length=100,
        required=False,
        label=_('Campus ID / Dorm or Department'),
        help_text=_('Optional: helps identify your main campus location (e.g. Block 42, Ag. Engineering)')
    )
    preferred_language = forms.ChoiceField(
        choices=User.LANGUAGE_CHOICES,
        initial='en',
        label=_('Preferred Language'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'campus_id_or_dorm',
            'preferred_language',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'role':
                existing_classes = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f"{existing_classes} form-control".strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('An account with this email already exists.'))
        return email


class UserProfileForm(forms.ModelForm):
    """
    Profile update form for existing users.
    """
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'campus_id_or_dorm',
            'preferred_language',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'campus_id_or_dorm': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_language': forms.Select(attrs={'class': 'form-select'}),
        }
