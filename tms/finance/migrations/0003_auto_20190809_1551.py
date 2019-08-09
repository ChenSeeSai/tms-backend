# Generated by Django 2.2.1 on 2019-08-09 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_etccardchargehistory_etccardusagehistory_fuelcardchargehistory_fuelcardusagehistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='etccard',
            name='issued_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fuelcard',
            name='issued_on',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='etccard',
            name='balance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='fuelcard',
            name='balance',
            field=models.FloatField(default=0),
        ),
    ]
