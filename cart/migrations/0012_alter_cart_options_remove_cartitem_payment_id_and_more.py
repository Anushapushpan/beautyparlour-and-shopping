# Generated by Django 4.1.7 on 2023-04-16 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_remove_cartitem_razorpay_payment_signature'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={},
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='razorpay_payment_id',
        ),
    ]
