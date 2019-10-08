# Generated by Django 2.2.1 on 2019-10-08 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyPolicyRead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_read', models.BooleanField(default=False)),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='security.CompanyPolicy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]