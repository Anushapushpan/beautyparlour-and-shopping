# Generated by Django 4.1.7 on 2023-04-16 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_order_razorpay_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
