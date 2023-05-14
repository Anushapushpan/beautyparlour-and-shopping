# Generated by Django 3.2.14 on 2023-03-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ParlourApp', '0009_gallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Expired', 'Expired')], default='Pending', max_length=150),
        ),
    ]
