import calendar
import csv
import datetime

from django.contrib import admin

# Register your models here.
from django.db.models import Sum
from django.http import HttpResponse

from cart.models import Cart, CartItem, Order, Profile, Orderitem, ProductReview


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'cart', 'quantity', 'active','is_paid','razorpay_order_id']


admin.site.register(CartItem, CartItemAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id','user', 'date_added']


admin.site.register(Cart, CartAdmin)



class OrderitemInline(admin.TabularInline):
    model = Orderitem
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price','payment_mode','order_id','status','tracking_no','created_at','estimated_delivery','city']
    list_editable = ['status']
    search_fields = ['order_id']
    actions = ['generate_daily_report','generate_monthly_report']

    def generate_daily_report(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="daily_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Total'])

        orders = queryset.order_by('created_at')

        current_date = None
        total_payment = 0

        for order in orders:
            order_date = order.created_at.date()
            if order_date != current_date:
                if current_date:
                    writer.writerow([current_date.strftime('%Y-%m-%d'), total_payment])
                current_date = order_date
                total_payment = 0
            total_payment += order.total_price

        if current_date:
            writer = csv.writer(response, dialect='excel')
            writer.writerow([current_date.strftime('%Y-%m-%d'), total_payment])

        return response

    generate_daily_report.short_description = "Generate daily payment report"

    def generate_monthly_report(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="monthly_payment_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Month/Year', 'Total Payment'])

        monthly_totals = {}

        for order in queryset:
            order_month = datetime.date(order.created_at.year, order.created_at.month, 1)
            if order_month.strftime('%Y-%m') not in monthly_totals:
                monthly_totals[order_month.strftime('%Y-%m')] = 0
            monthly_totals[order_month.strftime('%Y-%m')] += order.total_price

        for month, total_payment in monthly_totals.items():
            writer.writerow([month, total_payment])

        return response

    generate_monthly_report.short_description = "Generate monthly payment report"


admin.site.register(Order, OrderAdmin)


class OrderitemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product','price','quantity','total_price']

admin.site.register(Orderitem, OrderitemAdmin)
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
admin.site.register(Profile, ProfileAdmin)

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','rating','date_created']
    search_fields = ['product__name']
admin.site.register(ProductReview, ProductReviewAdmin)
