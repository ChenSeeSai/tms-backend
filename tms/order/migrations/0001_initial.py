# Generated by Django 2.2.1 on 2019-11-07 16:23

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import month.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hr', '0001_initial'),
        ('info', '0001_initial'),
        ('route', '0001_initial'),
        ('vehicle', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routes', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveIntegerField(), size=None)),
                ('progress', models.PositiveIntegerField(default=1)),
                ('started_on', models.DateTimeField(blank=True, null=True)),
                ('finished_on', models.DateTimeField(blank=True, null=True)),
                ('total_mileage', models.FloatField(default=0)),
                ('empty_mileage', models.FloatField(default=0)),
                ('heavy_mileage', models.FloatField(default=0)),
                ('highway_mileage', models.FloatField(blank=True, null=True)),
                ('normalway_mileage', models.FloatField(blank=True, null=True)),
                ('is_paid', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-finished_on',),
            },
        ),
        migrations.CreateModel(
            name='JobStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_unit_price', models.FloatField(default=0)),
                ('step', models.PositiveIntegerField()),
                ('arrived_station_on', models.DateTimeField(blank=True, null=True)),
                ('started_working_on', models.DateTimeField(blank=True, null=True)),
                ('finished_working_on', models.DateTimeField(blank=True, null=True)),
                ('departure_station_on', models.DateTimeField(blank=True, null=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Job')),
            ],
            options={
                'ordering': ['job', 'step'],
            },
        ),
        migrations.CreateModel(
            name='JobStationProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_time', models.DateTimeField(blank=True, null=True)),
                ('branch', models.PositiveIntegerField(default=0)),
                ('mission_weight', models.FloatField(default=0)),
                ('weight', models.FloatField(default=0)),
                ('man_hole', models.CharField(max_length=100)),
                ('branch_hole', models.CharField(max_length=100)),
                ('job_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.JobStation')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Product')),
            ],
            options={
                'ordering': ['job_station', 'branch'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('alias', models.CharField(blank=True, max_length=100, null=True)),
                ('order_source', models.CharField(choices=[('I', '内部'), ('C', 'App')], default='I', max_length=1)),
                ('status', models.CharField(choices=[('P', '未开始'), ('I', '已开始'), ('C', '已完成')], default='P', max_length=1)),
                ('arrangement_status', models.CharField(choices=[('P', '未派车'), ('I', '派车中'), ('C', '派车完')], default='P', max_length=1)),
                ('invoice_ticket', models.BooleanField(default=False)),
                ('tax_rate', models.FloatField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('loading_due_time', models.DateTimeField(blank=True, null=True)),
                ('is_same_station', models.BooleanField(default=False)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='charge_orders', to='hr.StaffProfile')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='hr.CustomerProfile')),
                ('loading_station', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_as_loading_station', to='info.Station')),
            ],
            options={
                'ordering': ['-updated'],
            },
        ),
        migrations.CreateModel(
            name='QualityCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.PositiveIntegerField(default=0)),
                ('density', models.FloatField(default=0)),
                ('additive', models.FloatField(default=0)),
                ('volume', models.FloatField(default=0)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quality_checks', to='order.Job')),
            ],
        ),
        migrations.CreateModel(
            name='OrderReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', month.models.MonthField()),
                ('orders', models.PositiveIntegerField(default=0)),
                ('weights', models.FloatField(default=0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_reports', to='hr.CustomerProfile')),
            ],
            options={
                'ordering': ('-month',),
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(default=0)),
                ('weight_measure_unit', models.CharField(choices=[('L', '公升'), ('T', '吨')], default='T', max_length=1)),
                ('arranged_weight', models.FloatField(default=0)),
                ('delivered_weight', models.FloatField(default=0)),
                ('is_split', models.BooleanField(default=False)),
                ('is_pump', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField(default=0)),
                ('adjustment', models.FloatField(default=0)),
                ('status', models.PositiveIntegerField(choices=[(0, '待更新'), (1, '待对账'), (2, '待开票'), (3, '待结算'), (4, '结算')], default=0)),
                ('job_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.JobStation')),
            ],
        ),
        migrations.CreateModel(
            name='OrderCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('weight', models.FloatField(default=0)),
                ('is_split', models.BooleanField(default=False)),
                ('is_pump', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Product')),
            ],
            options={
                'ordering': ('-updated',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(through='order.OrderProduct', to='info.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='quality_station',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_as_quality_station', to='info.Station'),
        ),
        migrations.AddField(
            model_name='order',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='route.Route'),
        ),
        migrations.CreateModel(
            name='LoadingStationProductCheck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('weight', models.FloatField(default=0)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loading_checks', to='order.Job')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoadingStationDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ImageField(upload_to='')),
                ('loading_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='order.LoadingStationProductCheck')),
            ],
        ),
        migrations.CreateModel(
            name='JobWorker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_type', models.CharField(choices=[('D', '司机'), ('E', '押运员')], default='D', max_length=1)),
                ('started_on', models.DateTimeField(blank=True, null=True)),
                ('finished_on', models.DateTimeField(blank=True, null=True)),
                ('assigned_on', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Job')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('job', '-assigned_on'),
            },
        ),
        migrations.CreateModel(
            name='JobStationProductDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ImageField(upload_to='')),
                ('job_station_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='order.JobStationProduct')),
            ],
        ),
        migrations.AddField(
            model_name='jobstation',
            name='products',
            field=models.ManyToManyField(through='order.JobStationProduct', to='info.Product'),
        ),
        migrations.AddField(
            model_name='jobstation',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='info.Station'),
        ),
        migrations.CreateModel(
            name='JobReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', month.models.MonthField()),
                ('total_mileage', models.PositiveIntegerField(default=0)),
                ('empty_mileage', models.PositiveIntegerField(default=0)),
                ('heavy_mileage', models.PositiveIntegerField(default=0)),
                ('highway_mileage', models.PositiveIntegerField(default=0)),
                ('normalway_mileage', models.PositiveIntegerField(default=0)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-month',),
            },
        ),
        migrations.AddField(
            model_name='job',
            name='associated_workers',
            field=models.ManyToManyField(related_name='associated_jobs', through='order.JobWorker', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='job',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='order.Order'),
        ),
        migrations.AddField(
            model_name='job',
            name='rest_place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='jobs_as_rest_place', to='info.Station'),
        ),
        migrations.AddField(
            model_name='job',
            name='stations',
            field=models.ManyToManyField(through='order.JobStation', to='info.Station'),
        ),
        migrations.AddField(
            model_name='job',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='vehicle.Vehicle'),
        ),
    ]
