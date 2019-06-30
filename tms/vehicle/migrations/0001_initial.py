# Generated by Django 2.2.1 on 2019-06-30 23:28

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('model', models.CharField(choices=[('T', '牵引车'), ('S', '半挂罐车')], default='T', max_length=1)),
                ('plate_num', models.CharField(max_length=100, unique=True)),
                ('identifier_code', models.CharField(max_length=100)),
                ('brand', models.CharField(choices=[('T', '通华'), ('L', '解放'), ('Y', '扬州中集')], default='T', max_length=1)),
                ('use_for', models.CharField(blank=True, max_length=100, null=True)),
                ('total_load', models.DecimalField(decimal_places=3, max_digits=7)),
                ('actual_load', models.DecimalField(decimal_places=3, max_digits=7)),
                ('affiliation_unit', models.CharField(blank=True, max_length=100, null=True)),
                ('use_started_on', models.DateField(blank=True, null=True)),
                ('use_expires_on', models.DateField(blank=True, null=True)),
                ('service_area', models.CharField(blank=True, max_length=100, null=True)),
                ('obtain_method', models.CharField(blank=True, max_length=100, null=True)),
                ('attribute', models.CharField(blank=True, max_length=100, null=True)),
                ('cert_type', models.CharField(blank=True, max_length=100, null=True)),
                ('cert_id', models.CharField(blank=True, max_length=100, null=True)),
                ('cert_authority', models.CharField(blank=True, max_length=100, null=True)),
                ('cert_registered_on', models.DateField(blank=True, null=True)),
                ('cert_active_on', models.DateField(blank=True, null=True)),
                ('cert_expires_on', models.DateField(blank=True, null=True)),
                ('insurance_active_on', models.DateField(blank=True, null=True)),
                ('insurance_expires_on', models.DateField(blank=True, null=True)),
                ('branches', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), size=None)),
                ('engine_model', models.CharField(blank=True, max_length=100, null=True)),
                ('engine_power', models.PositiveIntegerField(blank=True, null=True)),
                ('transmission_model', models.CharField(blank=True, max_length=100, null=True)),
                ('engine_displacement', models.CharField(blank=True, max_length=100, null=True)),
                ('tire_rules', models.CharField(blank=True, max_length=100, null=True)),
                ('tank_material', models.CharField(blank=True, max_length=100, null=True)),
                ('is_gps_installed', models.BooleanField(default=False)),
                ('is_gps_working', models.BooleanField(default=False)),
                ('with_pump', models.BooleanField(default=False)),
                ('main_car_size', models.CharField(blank=True, max_length=100, null=True)),
                ('main_car_color', models.CharField(blank=True, max_length=100, null=True)),
                ('trailer_car_size', models.CharField(blank=True, max_length=100, null=True)),
                ('trailer_car_color', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('A', 'Available'), ('P', 'In Work'), ('R', 'Repair')], default='A', max_length=1)),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
        migrations.CreateModel(
            name='VehicleUserBind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bind_method', models.CharField(choices=[('A', 'By Admin'), ('J', 'By Job')], default='A', max_length=1)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles_as_driver', to=settings.AUTH_USER_MODEL)),
                ('escort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles_as_escort', to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.Vehicle')),
            ],
            options={
                'unique_together': {('vehicle', 'driver', 'escort')},
            },
        ),
        migrations.CreateModel(
            name='VehicleMaintenanceRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_time', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.CharField(choices=[('R', 'Repair')], max_length=1)),
                ('maintenance_from', models.DateField()),
                ('maintenance_to', models.DateField()),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.Vehicle')),
            ],
            options={
                'ordering': ['approved', '-approved_time', '-request_time'],
                'unique_together': {('vehicle', 'approved')},
            },
        ),
    ]
