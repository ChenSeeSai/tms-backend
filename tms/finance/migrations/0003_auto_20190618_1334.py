# Generated by Django 2.2.1 on 2019-06-18 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0005_auto_20190617_1518'),
        ('finance', '0002_orderpayment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fuelcard',
            old_name='parent',
            new_name='master',
        ),
        migrations.AddField(
            model_name='fuelcard',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehicle.Vehicle'),
        ),
    ]
