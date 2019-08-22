# Generated by Django 2.2.1 on 2019-08-22 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_auto_20190823_0540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadingstationproductcheck',
            name='job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='loading_check', to='order.Job'),
        ),
        migrations.AlterField(
            model_name='qualitycheck',
            name='job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='quality_check', to='order.Job'),
        ),
    ]
