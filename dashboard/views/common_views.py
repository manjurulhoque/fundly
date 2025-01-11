from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, View
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render

from campaign.models import Campaign, Donation


class DashboardView(View):
    template_name = "dashboard/home.html"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Get date 30 days ago
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Get user campaigns
        user_campaigns = Campaign.objects.filter(user=self.request.user)
        
        # Get daily donations for last 30 days
        daily_donations = Donation.objects.filter(
            campaign__user=self.request.user,
            date__gte=thirty_days_ago,
            approved=True
        ).annotate(
            day=TruncDay('date')
        ).values('day').annotate(
            total=Sum('donation'),
            count=Count('id')
        ).order_by('day')
        
        # Prepare chart data
        dates = []
        amounts = []
        counts = []
        
        current_date = thirty_days_ago.date()
        end_date = timezone.now().date()
        
        # Create lookup dictionary
        donations_dict = {
            d['day'].strftime('%Y-%m-%d'): {'total': d['total'], 'count': d['count']}
            for d in daily_donations
        }

        while current_date <= end_date:
            dates.append(current_date.strftime('%Y-%m-%d'))
            current_datetime = timezone.make_aware(
                timezone.datetime.combine(current_date, timezone.datetime.min.time())
            )
            day_data = donations_dict.get(current_datetime.strftime('%Y-%m-%d'), {'total': 0, 'count': 0})
            amounts.append(float(day_data['total'] or 0))
            counts.append(day_data['count'])
            current_date += timedelta(days=1)

        context = {
            "active_campaigns": user_campaigns.filter(status="active").count(),
            "total_raised": Donation.objects.filter(
                campaign__user=self.request.user, approved=True
            ).aggregate(Sum("donation"))["donation__sum"] or 0,
            "total_donations": Donation.objects.filter(
                campaign__user=self.request.user, approved=True
            ).count(),
            "chart_dates": dates,
            "chart_amounts": amounts,
            "chart_counts": counts,
        }
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class CampaignListView(ListView):
    template_name = "dashboard/campaigns.html"
    context_object_name = "campaigns"
    paginate_by = 10

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return (
            Campaign.objects.filter(user=self.request.user)
            .prefetch_related("donation_set")
            .order_by("-date")
        )


class DonationListView(ListView):
    template_name = "dashboard/donations.html"
    context_object_name = "donations"
    paginate_by = 10

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Donation.objects.filter(
            campaign__user=self.request.user
        ).select_related(
            'campaign'
        ).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        donations = self.get_queryset()
        context.update({
            'total_donations': donations.count(),
            'total_amount': donations.aggregate(Sum('donation'))['donation__sum'] or 0,
            'approved_donations': donations.filter(approved=True).count(),
            'pending_donations': donations.filter(approved=False).count(),
        })
        return context
