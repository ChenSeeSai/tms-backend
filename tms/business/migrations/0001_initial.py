# Generated by Django 2.2.1 on 2019-08-26 14:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicle', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('R', '假期'), ('V', '车辆修理')], default='R', max_length=1)),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_time', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['approved', '-approved_time', '-request_time'],
            },
        ),
        migrations.CreateModel(
            name='VehicleRepairRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('B', '查看刹车')], default='B', max_length=1)),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_repair_request', to='business.BasicRequest')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehicle.Vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='RestRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('I', '病假'), ('P', '私事')], default='I', max_length=1)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rest_request', to='business.BasicRequest')),
            ],
        ),
        migrations.CreateModel(
            name='RequestDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ImageField(upload_to='')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='business.BasicRequest')),
            ],
        ),
        migrations.CreateModel(
            name='RequestCC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cc_type', models.CharField(choices=[('P', '职位'), ('W', '人员')], default='W', max_length=1)),
                ('is_read', models.BooleanField(default=False)),
                ('read_time', models.DateTimeField(auto_now=True)),
                ('cc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BasicRequest')),
            ],
        ),
        migrations.CreateModel(
            name='RequestApprover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approver_type', models.CharField(choices=[('P', '职位'), ('W', '人员')], default='W', max_length=1)),
                ('approved', models.BooleanField(default=False)),
                ('approved_time', models.DateTimeField(auto_now=True)),
                ('step', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, null=True)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BasicRequest')),
            ],
        ),
        migrations.AddField(
            model_name='basicrequest',
            name='approvers',
            field=models.ManyToManyField(related_name='request_as_approver', through='business.RequestApprover', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basicrequest',
            name='ccs',
            field=models.ManyToManyField(related_name='request_as_cc', through='business.RequestCC', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basicrequest',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_requests', to=settings.AUTH_USER_MODEL),
        ),
    ]
