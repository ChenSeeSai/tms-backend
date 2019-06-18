# Generated by Django 2.2.1 on 2019-06-17 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('vehicle', '0002_vehiclemaintenancerequest'),
        ('job', '0003_auto_20190614_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherParkingPlaceRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_time', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_parkings', to='account.DriverProfile')),
                ('escort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_parkings', to='account.EscortProfile')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='job.Job')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_parkings', to='vehicle.Vehicle')),
            ],
            options={
                'ordering': ['approved', '-approved_time', '-request_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EscortChangeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_time', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('change_time', models.DateTimeField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Job')),
                ('new_escort', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.EscortProfile')),
            ],
            options={
                'ordering': ['approved', '-approved_time', '-request_time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DriverChangeRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_time', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('change_time', models.DateTimeField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Job')),
                ('new_driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.DriverProfile')),
            ],
            options={
                'ordering': ['approved', '-approved_time', '-request_time'],
                'abstract': False,
            },
        ),
    ]