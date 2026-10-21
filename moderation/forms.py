"""
Forms for moderation app.
Price discrepancy reporting by students and resolution by moderators.
"""

from decimal import Decimal
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import PriceReport


class PriceReportForm(forms.ModelForm):
    """
    Form allowing students and community members to report pricing errors or out-of-stock items.
    """
    class Meta:
        model = PriceReport
        fields = [
            'report_type',
            'observed_price',
            'comment',
            'proof_image',
        ]
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'observed_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': _('e.g. 85.00 (leave blank if not applicable)'),
                'step': '0.50',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Please provide details: what price were you charged, or what was the shop keeper response?')
            }),
            'proof_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', '').strip()
        if len(comment) < 10:
            raise forms.ValidationError(_('Please provide a slightly more descriptive explanation (at least 10 characters).'))
        return comment


class ModerationResolutionForm(forms.Form):
    """
    Form for moderators to resolve or dismiss a report with notes.
    """
    action = forms.ChoiceField(
        choices=[
            ('resolve', _('Mark Resolved (Action Taken / Verified)')),
            ('dismiss', _('Dismiss Report (Invalid / Disputed)')),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    resolution_note = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': _('Explain the resolution action taken (e.g. contacted shop owner, verified price update).')
        })
    )
