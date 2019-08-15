# Generated by Django 2.2.1 on 2019-08-15 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicle', '0006_auto_20190815_1412'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='actual_load2',
            new_name='actual_load_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='brand2',
            new_name='brand_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='cert_active_on2',
            new_name='cert_active_on_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='cert_authority2',
            new_name='cert_authority_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='cert_expires_on2',
            new_name='cert_expires_on_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='cert_id2',
            new_name='cert_id_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='cert_registered_on2',
            new_name='cert_registered_on_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='cert_type2',
            new_name='cert_type_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='identifier_code2',
            new_name='identifier_code_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='insurance_active_on2',
            new_name='insurance_active_on_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='insurance_expires_on2',
            new_name='insurance_expires_on_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='model2',
            new_name='model_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='plate_num2',
            new_name='plate_num_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='total_load2',
            new_name='total_load_2',
        ),
        migrations.RenameField(
            model_name='vehicle',
            old_name='use_for2',
            new_name='use_for_2',
        ),
    ]
