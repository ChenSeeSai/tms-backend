# Generated by Django 2.2.1 on 2019-11-01 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0003_auto_20191030_2358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehiclecheckhistory',
            options={'ordering': ['driver', '-updated']},
        ),
    ]
