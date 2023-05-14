from django.contrib import admin

# Register your models here.
from ShoppingApp.models import Category, Product, Shades


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price','discount','discounted_price','stock','available','is_tryon_eligible','created','updated']
    list_editable = ['price','discount','stock','available','is_tryon_eligible']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_per_page = 20


admin.site.register(Product, ProductAdmin)
admin.site.register(Shades)
