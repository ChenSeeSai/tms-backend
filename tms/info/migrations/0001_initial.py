# Generated by Django 2.2.1 on 2019-09-02 18:37

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlarmSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('rapid_acceleration', models.PositiveIntegerField(default=0)),
                ('rapid_deceleration', models.PositiveIntegerField(default=0)),
                ('sharp_turn', models.PositiveIntegerField(default=0)),
                ('over_speed', models.PositiveIntegerField(default=0)),
                ('over_speed_duration', models.PositiveIntegerField(default=0)),
                ('rotation_speed', models.PositiveIntegerField(default=0)),
                ('vehicle_review_duration', models.PositiveIntegerField(default=0)),
                ('driver_license_duration', models.PositiveIntegerField(default=0)),
                ('vehicle_operation_duration', models.PositiveIntegerField(default=0)),
                ('vehicle_insurance_duration', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-updated',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('code', models.CharField(max_length=100, unique=True)),
                ('price', models.FloatField(default=0)),
                ('unit_weight', models.PositiveIntegerField(default=1)),
                ('weight_measure_unit', models.CharField(choices=[('L', '公升'), ('T', '吨')], default='T', max_length=1)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('level', models.PositiveIntegerField(default=3)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-updated',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('path', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), size=None)),
                ('policy', models.PositiveIntegerField(choices=[(0, '最快捷模式'), (1, '最经济模式'), (2, '最短距离模式')], default=0)),
                ('distance', models.FloatField(default=0)),
            ],
            options={
                'ordering': ('-updated',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('contact', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile', models.CharField(blank=True, max_length=30, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('station_type', models.CharField(choices=[('L', '装货地'), ('U', '卸货地'), ('Q', '质检点'), ('O', '合作油站'), ('B', '黑点'), ('P', '合法停车区域'), ('R', '供应商'), ('C', 'Custom')], max_length=1)),
                ('longitude', models.FloatField(default=0)),
                ('latitude', models.FloatField(default=0)),
                ('radius', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.FloatField(default=0)),
                ('working_time', models.PositiveIntegerField(blank=True, null=True)),
                ('working_time_measure_unit', models.CharField(choices=[('M', '分钟'), ('H', '小时')], default='H', max_length=1)),
                ('average_time', models.PositiveIntegerField(blank=True, null=True)),
                ('average_time_measure_unit', models.CharField(choices=[('M', '分钟'), ('H', '小时')], default='H', max_length=1)),
                ('price_vary_duration', models.PositiveIntegerField(blank=True, null=True)),
                ('price_vary_duration_unit', models.CharField(choices=[('W', '周'), ('M', '月'), ('Y', '年')], default='M', max_length=1)),
                ('notification_message', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('customers', models.ManyToManyField(to='hr.CustomerProfile')),
                ('products', models.ManyToManyField(to='info.Product')),
            ],
            options={
                'ordering': ['station_type', '-updated'],
            },
        ),
        migrations.CreateModel(
            name='TransportationDistance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('distance', models.FloatField(default=0)),
                ('average_time', models.FloatField(default=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('end_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_points', to='info.Station')),
                ('start_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_points', to='info.Station')),
            ],
            options={
                'ordering': ('-updated',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.ProductCategory'),
        ),
    ]
