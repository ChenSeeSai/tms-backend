# Generated by Django 2.2.1 on 2019-06-18 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hr', '0003_auto_20190618_0845'),
        ('vehicle', '0005_auto_20190617_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_company', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=100)),
                ('key', models.CharField(max_length=100)),
                ('last_charge_date', models.DateField(blank=True, null=True)),
                ('balance', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.Department')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='finance.FuelCard')),
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
                ('number', models.CharField(max_length=100)),
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
    ]
