from django import forms
from django.core.exceptions import ValidationError

from .models import *


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ('user', 'status', 'is_deleted')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.status = kwargs.pop('status', None)
        super(CampaignForm, self).__init__(*args, **kwargs)
        self.fields['deadline'].input_formats = ['%Y-%m-%d']

    def clean_user(self):
        return self.user

    def clean_status(self):
        return self.status


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        exclude = ('date', 'approved', 'campaign')

    def clean_donation(self):
        amount = self.cleaned_data['donation']
        if amount < 5:
            raise ValidationError("Amount must be greater or equal to $5")
        return amount
