# Generated by Django 2.2.1 on 2019-08-17 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0010_vehicleafterdrivingdocuments_vehiclebeforedrivingdocuments_vehicledrivingdocuments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VehicleDrivingDocuments',
            new_name='VehicleAfterDrivingDocument',
        ),
        migrations.RenameModel(
            old_name='VehicleBeforeDrivingDocuments',
            new_name='VehicleBeforeDrivingDocument',
        ),
        migrations.RenameModel(
            old_name='VehicleAfterDrivingDocuments',
            new_name='VehicleDrivingDocument',
        ),
        migrations.AlterField(
            model_name='vehicleafterdrivingdocument',
            name='vehicle_check_history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.VehicleAfterDrivingCheckHistory'),
        ),
        migrations.AlterField(
            model_name='vehicledrivingdocument',
            name='vehicle_check_history',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.VehicleDrivingCheckHistory'),
        ),
    ]
