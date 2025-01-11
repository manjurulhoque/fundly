from django.urls import path

from .views.admin_views import AdminDashboardView, AdminCampaignsView

app_name = 'admin_dashboard'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='home'),
    path('campaigns/', AdminCampaignsView.as_view(), name='campaigns'),
]
