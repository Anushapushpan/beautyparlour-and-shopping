from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models
from django.forms import Textarea, TextInput

from .models import Appointment, Category, Service, Time_slot, Gallery


# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'status', 'date', 'time', 'created_at', 'updated_at')
    list_editable = ['status']
    search_fields = ['service__name','user__username']


class Time_slotAdmin(admin.ModelAdmin):
    list_display = ('slot', 'status')
    list_editable = ['status']


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Time_slot, Time_slotAdmin)
admin.site.register(Category)
admin.site.register(Gallery)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price', 'created_at','available')
    list_editable = ['available']

admin.site.register(Service, ServiceAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "time", "approved")
    list_filter = ("approved", "date")
    ordering = ("date", "time")
    search_fields = ("user_email", "user_name")
