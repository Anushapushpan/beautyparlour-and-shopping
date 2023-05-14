from decimal import Decimal

from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='category')

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'
    def get_url(self):
        return reverse('ShoppingApp:products_by_category', args=[self.slug])
    def __str__(self):
        return  '{}'.format(self.name)

class Product(models.Model):
    name=models.CharField(max_length=250, unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.IntegerField()
    discounted_price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='product')
    is_tryon_eligible = models.BooleanField(default=False)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        discount_decimal = Decimal(str(self.discount))
        self.discounted_price = self.price - (self.price * (discount_decimal / 100))
        super(Product, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('ShoppingApp:prodCatdetail',args=[self.category.slug, self.slug])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_tryon_eligible'] = self.object.is_tryon_eligible
        return context

    class Meta:
        ordering=('name',)
        verbose_name='product'
        verbose_name_plural='products'

    def __str__(self):
        return  '{}'.format(self.name)

class Shades(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shade1 = models.CharField(max_length=250,blank=True)
    shade2 = models.CharField(max_length=250,blank=True)
    shade3 = models.CharField(max_length=250,blank=True)
    shade4 = models.CharField(max_length=250,blank=True)
    shade5 = models.CharField(max_length=250,blank=True)