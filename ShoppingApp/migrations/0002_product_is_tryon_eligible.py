# Generated by Django 3.2.14 on 2023-02-24 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShoppingApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_tryon_eligible',
            field=models.BooleanField(default=False),
        ),
    ]
