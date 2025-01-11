from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, UpdateView
from django.db.models import Sum
from django.contrib import messages
from django.urls import reverse_lazy

from dashboard.mixins import SuperUserRequiredMixin
from campaign.models import Campaign, Donation, CampaignStatusChoices
from campaign.forms import CampaignForm

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
            'active_campaigns': Campaign.objects.filter(
                status=CampaignStatusChoices.APPROVED
            ).count(),
            'total_raised': Donation.objects.filter(
                approved=True
            ).aggregate(Sum('donation'))['donation__sum'] or 0
        })
        return context


class AdminDonationsView(SuperUserRequiredMixin, View):
    def get(self, request):
        return render(request, "dashboard/admin/donations.html")


class AdminCampaignEditView(SuperUserRequiredMixin, UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "dashboard/admin/campaign-edit.html"
    success_url = reverse_lazy('admin_dashboard:campaigns')
    
    def form_valid(self, form):
        messages.success(self.request, 'Campaign updated successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)


class AdminCampaignDeleteView(SuperUserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        campaign_id = request.POST.get('id')
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            campaign.status = CampaignStatusChoices.DELETED
            campaign.save()
            messages.success(request, 'Campaign deleted successfully!')
        except Campaign.DoesNotExist:
            messages.error(request, 'Campaign not found!')
        return redirect('admin_dashboard:campaigns')