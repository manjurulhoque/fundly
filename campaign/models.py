import hashlib
import uuid
from datetime import datetime
from django.db import models
from django.utils.http import urlencode
from django.utils.timezone import now
from django.templatetags.static import static
from django.db.models import Sum
from accounts.models import User
from core.models import Category


class CampaignStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    DELETED = "deleted", "Deleted"


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now, blank=True)
    status = models.CharField(
        max_length=20,
        choices=CampaignStatusChoices.choices,
        default=CampaignStatusChoices.PENDING,
    )
    image = models.ImageField(upload_to="campaigns")
    goal = models.IntegerField()
    location = models.CharField(max_length=150)
    deadline = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def image_url(self):
        return (
            self.image.url
            if self.image
            else "https://placehold.co/600x400?text=No+Image"
        )

    def days_remaining(self):
        delta = self.deadline - datetime.now().date()
        return delta.days

    @property
    def total_raised(self):
        return (
            self.donation_set.filter(approved=True).aggregate(Sum("donation"))[
                "donation__sum"
            ]
            or 0
        )
  
    
    @property 
    def raised_percentage(self):
        return round((self.total_raised / self.goal) * 100,2)


    @property
    def total_donations(self):
        return self.donation_set.aggregate(Sum("donation"))["donation__sum"] or 0

    
    @property
    def total_donations_approved(self):
        return (
            self.donation_set.filter(approved=True).aggregate(Sum("donation"))[
                "donation__sum"
            ]
            or 0
        )
    
    
    @property
    def total_donations_pending(self):
        return (
            self.donation_set.filter(approved=False).aggregate(Sum("donation"))[
                "donation__sum"
            ]
            or 0
        )


    def total_donations_rejected(self):
        return (
            self.donation_set.filter(approved=False).aggregate(Sum("donation"))[
                "donation__sum"
            ]
            or 0
        )


    def get_status_display(self):
        return self.status.upper()


class Donation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    donation = models.PositiveIntegerField()
    anonymous = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return "{} donate {}".format(self.fullname, self.donation)

    @property
    def name(self):
        return self.fullname if self.anonymous == 0 else "Anonymous"

    @property
    def avatar(self):
        default = static("img/default.jpg")
        size = 40
        query_string = urlencode(
            {
                "s": str(size),
            }
        )

        url_base = "https://www.gravatar.com/"
        email_hash = hashlib.md5(self.email.strip().lower().encode("utf-8")).hexdigest()

        # Build url
        url = "{base}avatar/{hash}.jpg?{qs}".format(
            base=url_base, hash=email_hash, qs=query_string
        )
        return default if self.anonymous == 0 else url

    @property
    def admin_earnings(self):
        return self.donation * 0.05
    
    @property
    def admin_earnings_formatted(self):
        return f"${self.admin_earnings:.2f}"
