# Generated by Django 4.2.6 on 2023-10-18 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DolarPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, default=0)),
                ('date_registered', models.DateField(blank=True, default=dashboard.models.get_current_date)),
            ],
        ),
    ]
