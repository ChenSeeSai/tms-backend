# Generated by Django 2.2.1 on 2019-08-28 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestapprover',
            name='approved',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='requestapprover',
            name='approved_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]