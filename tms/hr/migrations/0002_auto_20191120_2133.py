# Generated by Django 2.2.1 on 2019-11-20 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverlicense',
            name='work_license',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='driverlicense',
            name='work_license_expires_on',
            field=models.DateField(blank=True, null=True),
        ),
    ]