# Generated by Django 2.2.1 on 2019-08-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_auto_20190807_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='station',
            name='latitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='station',
            name='longitude',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='station',
            name='station_type',
            field=models.CharField(choices=[('L', '装货地'), ('U', '卸货地'), ('Q', '质检点'), ('O', '合作油站'), ('B', '黑点'), ('P', '合法停车区域'), ('R', '供应商')], max_length=1),
        ),
    ]