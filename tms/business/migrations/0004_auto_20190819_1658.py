# Generated by Django 2.2.1 on 2019-08-19 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20190819_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restrequest',
            name='category',
            field=models.CharField(choices=[('I', '病假'), ('P', '私事')], default='I', max_length=1),
        ),
    ]