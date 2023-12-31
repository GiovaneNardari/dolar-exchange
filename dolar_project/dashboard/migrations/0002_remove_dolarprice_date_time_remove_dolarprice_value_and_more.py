# Generated by Django 4.2.6 on 2023-10-29 15:48

import dashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dolarprice',
            name='date_time',
        ),
        migrations.RemoveField(
            model_name='dolarprice',
            name='value',
        ),
        migrations.AddField(
            model_name='dolarprice',
            name='date_registered',
            field=models.DateField(blank=True, default=dashboard.models.get_current_date),
        ),
        migrations.AddField(
            model_name='dolarprice',
            name='price',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
