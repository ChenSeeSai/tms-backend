# Generated by Django 2.2.1 on 2019-09-02 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0015_auto_20190830_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayment',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]