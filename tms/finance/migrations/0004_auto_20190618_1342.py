# Generated by Django 2.2.1 on 2019-06-18 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_auto_20190618_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etccard',
            name='number',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='fuelcard',
            name='number',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]