# Generated by Django 2.2.1 on 2019-08-07 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_auto_20190807_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='level',
            field=models.PositiveIntegerField(default=3),
        ),
    ]
