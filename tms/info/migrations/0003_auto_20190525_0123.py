# Generated by Django 2.2.1 on 2019-05-25 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0002_auto_20190525_0122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['updated', 'created']},
        ),
    ]