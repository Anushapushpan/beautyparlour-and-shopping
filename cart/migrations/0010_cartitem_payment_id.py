# Generated by Django 4.1.7 on 2023-04-16 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_remove_order_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
