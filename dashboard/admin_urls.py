from django.urls import path

from .views.admin_views import (
    AdminDashboardView,
    AdminCampaignsView,
    AdminCampaignEditView,
    AdminCampaignDeleteView,
    AdminDonationsView,
    AdminCategoriesView,
    AdminCategoryCreateView,
    AdminCategoryUpdateView,
    AdminCategoryDeleteView,
    AdminMembersView,
    AdminMemberToggleView,
    AdminMemberDeleteView,
)

app_name = 'admin_dashboard'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='home'),
    path('campaigns/', AdminCampaignsView.as_view(), name='campaigns'),
    path('campaigns/edit/<uuid:pk>/', AdminCampaignEditView.as_view(), name='campaign-edit'),
    path('campaigns/delete/', AdminCampaignDeleteView.as_view(), name='campaign-delete'),
    
    path('donations/', AdminDonationsView.as_view(), name='donations'),
    
    path('categories/', AdminCategoriesView.as_view(), name='categories'),
    path('categories/create/', AdminCategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', AdminCategoryUpdateView.as_view(), name='category-edit'),
    path('categories/delete/', AdminCategoryDeleteView.as_view(), name='category-delete'),
    
    path('members/', AdminMembersView.as_view(), name='members'),
    path('members/toggle/', AdminMemberToggleView.as_view(), name='member-toggle'),
    path('members/delete/', AdminMemberDeleteView.as_view(), name='member-delete'),
]
