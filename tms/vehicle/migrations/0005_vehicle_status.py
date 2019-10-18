# Generated by Django 2.2.1 on 2019-10-19 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0004_remove_vehicle_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, 'Available'), (1, 'Under wheel'), (2, 'Repair')], default=0),
        ),
    ]