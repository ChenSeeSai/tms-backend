# Generated by Django 2.2.1 on 2019-05-24 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0004_remove_job_path'),
        ('road', '0002_auto_20190524_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='road.Route'),
        ),
    ]