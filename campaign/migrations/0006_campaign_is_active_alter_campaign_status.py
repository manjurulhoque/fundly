# Generated by Django 5.0.8 on 2025-01-11 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campaign", "0005_donation"),
    ]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="campaign",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("rejected", "Rejected"),
                    ("deleted", "Deleted"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
    ]
