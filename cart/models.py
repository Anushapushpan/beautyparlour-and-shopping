from datetime import timedelta, datetime
from decimal import Decimal

from django.db import models
from django.utils import timezone

from BeautyParlour import settings
from ShoppingApp.models import Product
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'Cart'
        # ordering = ['date_added']

    def __str__(self):
        return '{}'.format(self.cart_id)

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart= models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    active=models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50,null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table='CartItem'
    def sub_total(self):
        discounted_price = self.product.price * (Decimal(1) - (Decimal(self.product.discount) / Decimal(100)))
        return discounted_price * Decimal(self.quantity)
    def __str__(self):
        return '{}'.format(self.product)



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150,null=False)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    order_id = models.CharField(max_length=100, null=True, blank=True)
    orderstatuses = (
        ('Order Confirmed','Order Confirmed'),
        ('Out for shipping', 'Out for shipping'),
        ('On the way','On the way'),
        ('Completed', 'Completed'),
    )
    status = models.CharField(max_length=150,choices=orderstatuses,default='Order Confirmed')
    message = models.TextField(null=True,blank=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_delivery = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.pk and not self.estimated_delivery and self.created_at:
            self.estimated_delivery = self.created_at + timedelta(days=5)
        super(Order, self).save(*args, **kwargs)

class Orderitem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=True)

    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_no)

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=False)
    address = models.TextField(max_length=50, null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField()
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return str(self.id)


