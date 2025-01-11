from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView
from django.db.models import Sum

from dashboard.mixins import SuperUserRequiredMixin
from campaign.models import Campaign, Donation

class AdminDashboardView(SuperUserRequiredMixin, View):
    def get(self, request):
        return render(request, "dashboard/admin/dashboard.html")


class AdminCampaignsView(SuperUserRequiredMixin, ListView):
    model = Campaign
    template_name = "dashboard/admin/campaigns.html"
    context_object_name = "campaigns"
    paginate_by = 10
    
    def get_queryset(self):
        return Campaign.objects.select_related(
            'user', 'category'
        ).prefetch_related(
            'donation_set'
        ).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_campaigns': Campaign.objects.count(),
            'active_campaigns': Campaign.objects.filter(status='active').count(),
            'total_raised': Donation.objects.filter(
                approved=True
            ).aggregate(Sum('donation'))['donation__sum'] or 0
        })
        return context


class AdminDonationsView(SuperUserRequiredMixin, View):
    def get(self, request):
        return render(request, "dashboard/admin/donations.html")