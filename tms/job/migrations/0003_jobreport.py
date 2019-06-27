# Generated by Django 2.2.1 on 2019-06-27 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import month.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0002_auto_20190626_0635'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', month.models.MonthField()),
                ('total_mileage', models.PositiveIntegerField(blank=True, null=True)),
                ('empty_mileage', models.PositiveIntegerField(blank=True, null=True)),
                ('heavy_mileage', models.PositiveIntegerField(blank=True, null=True)),
                ('highway_mileage', models.PositiveIntegerField(blank=True, null=True)),
                ('normalway_mileage', models.PositiveIntegerField(blank=True, null=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]