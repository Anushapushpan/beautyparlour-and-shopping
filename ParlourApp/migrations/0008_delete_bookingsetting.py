# Generated by Django 3.2.14 on 2022-11-23 17:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParlourApp', '0007_rename_bookingsettings_bookingsetting'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookingSetting',
        ),
    ]
