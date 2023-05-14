

from django.conf import settings
from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False, unique=True)
    image = models.ImageField(upload_to='category')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False, unique=True)
    image = models.ImageField(upload_to='service')
    price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery')
    description = models.TextField(max_length=250,blank=True)


class Time_slot(models.Model):
    slot = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.slot


# Create An Appointmetment Form
class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    statuses = (
        ('Expired', 'Expired'),
        ('Approved', 'Approved'),
    )
    status = models.CharField(max_length=150,choices=statuses,default='Approved')
    time = models.ForeignKey(Time_slot, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
