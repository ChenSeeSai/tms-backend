# Generated by Django 2.2.1 on 2019-10-13 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_auto_20191012_2230'),
        ('order', '0008_jobstation_transport_unit_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(default=0)),
                ('distance', models.FloatField(default=0)),
                ('transport_unit_price', models.FloatField(default=0)),
                ('adjustment', models.FloatField(default=0)),
                ('status', models.PositiveIntegerField(choices=[(0, '待更新'), (1, '待对账'), (2, '待开票'), (3, '结算')], default='I')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Job')),
                ('loading_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_as_loading_station', to='info.Station')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='info.Product')),
                ('unloading_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments_as_unloading_station', to='info.Station')),
            ],
        ),
    ]
