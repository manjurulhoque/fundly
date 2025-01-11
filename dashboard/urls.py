from django.urls import path

from .views.common_views import DashboardView, CampaignListView, DonationListView

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('campaigns/', CampaignListView.as_view(), name='campaigns'),
    path('donations/', DonationListView.as_view(), name='donations'),
]
