# Generated by Django 2.2.5 on 2019-09-21 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_auto_20190921_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='deadline',
            field=models.DateField(),
        ),
    ]
