# Generated by Django 2.2.1 on 2019-07-28 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hr', '0001_initial'),
        ('vehicle', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=3, max_digits=7)),
                ('is_complete', models.BooleanField(default=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order')),
            ],
        ),
        migrations.CreateModel(
            name='FuelCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_company', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100, unique=True)),
                ('key', models.CharField(max_length=100)),
                ('last_charge_date', models.DateField(blank=True, null=True)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.Department')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='finance.FuelCard')),
                ('vehicle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vehicle.Vehicle')),
            ],
            options={
                'ordering': ['-last_charge_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ETCCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_company', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100, unique=True)),
                ('key', models.CharField(max_length=100)),
                ('last_charge_date', models.DateField(blank=True, null=True)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.Department')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.Vehicle')),
            ],
            options={
                'ordering': ['-last_charge_date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BillDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('bill', models.ImageField(upload_to='')),
                ('category', models.PositiveIntegerField(choices=[(0, '加油'), (1, '路票'), (2, '其他')])),
                ('sub_category', models.PositiveIntegerField(default=0)),
                ('detail_category', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bills', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['category'],
            },
        ),
    ]
