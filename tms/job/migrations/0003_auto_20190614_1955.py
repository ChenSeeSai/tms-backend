# Generated by Django 2.2.1 on 2019-06-14 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_auto_20190614_1551'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobbilldocument',
            old_name='document',
            new_name='bill',
        ),
    ]