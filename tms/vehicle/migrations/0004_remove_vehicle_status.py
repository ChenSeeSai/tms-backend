# Generated by Django 2.2.1 on 2019-10-19 00:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0003_auto_20191019_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='status',
        ),
    ]
