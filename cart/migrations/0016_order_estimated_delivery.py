# Generated by Django 4.1.7 on 2023-04-19 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0015_alter_order_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='estimated_delivery',
            field=models.DateField(null=True),
        ),
    ]
