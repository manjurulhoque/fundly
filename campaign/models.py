import uuid
from datetime import datetime
from django.db import models
from django.utils.timezone import now

from accounts.models import User
from core.models import Category


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now, blank=True)
    status = models.CharField(max_length=20, default='pending')
    image = models.ImageField(upload_to="campaigns")
    goal = models.IntegerField()
    location = models.CharField(max_length=150)
    deadline = models.DateField()

    def days_remaining(self):
        delta = self.deadline - datetime.now().date()
        return delta.days
