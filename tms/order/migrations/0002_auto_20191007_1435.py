# Generated by Django 2.2.1 on 2019-10-07 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobstation',
            name='due_time',
        ),
        migrations.AddField(
            model_name='jobstationproduct',
            name='due_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
