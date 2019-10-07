# Generated by Django 2.2.1 on 2019-10-07 12:01

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('info', '0001_initial'),
        ('vehicle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('is_g7_route', models.BooleanField(default=False)),
                ('map_path', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), null=True, size=None)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
                ('g7_path', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=2), null=True, size=None)),
                ('distance', models.FloatField(default=0)),
                ('end_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes_as_end_point', to='info.Station')),
                ('start_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes_as_start_point', to='info.Station')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicle.Vehicle')),
            ],
            options={
                'ordering': ('-updated',),
                'abstract': False,
            },
        ),
    ]
