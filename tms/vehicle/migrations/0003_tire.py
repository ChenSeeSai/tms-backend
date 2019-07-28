# Generated by Django 2.2.1 on 2019-07-28 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0002_fuelconsumption'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('model', models.CharField(max_length=100)),
                ('tire_type', models.CharField(max_length=100)),
                ('tread_depth', models.FloatField(default=0)),
                ('mileage_limit', models.PositiveIntegerField(default=0)),
                ('use_cycle', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('-updated',),
                'abstract': False,
            },
        ),
    ]