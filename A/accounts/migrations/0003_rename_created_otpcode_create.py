# Generated by Django 4.1.3 on 2023-01-31 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_otpcode_active_otpcode_expire_alter_otpcode_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otpcode',
            old_name='created',
            new_name='create',
        ),
    ]
