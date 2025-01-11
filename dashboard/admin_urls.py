from django.urls import path

from .views.admin_views import (
    AdminDashboardView,
    AdminCampaignsView,
    AdminCampaignEditView,
    AdminCampaignDeleteView,
    AdminDonationsView
)

app_name = 'admin_dashboard'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='home'),
    path('campaigns/', AdminCampaignsView.as_view(), name='campaigns'),
    path('campaigns/edit/<uuid:pk>/', AdminCampaignEditView.as_view(), name='campaign-edit'),
    path('campaigns/delete/', AdminCampaignDeleteView.as_view(), name='campaign-delete'),
    
    path('donations/', AdminDonationsView.as_view(), name='donations'),
]
