from decimal import Decimal

from django.db.models import Avg
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from ShoppingApp.models import Category, Product, Shades
from django.core.paginator import Paginator,EmptyPage,InvalidPage

#
from cart.models import ProductReview


def allProdCat(request, c_slug=None):

        c_page = None
        products_list = None
        if c_slug != None:
            c_page = get_object_or_404(Category, slug=c_slug)
            products_list = Product.objects.all().filter(category=c_page, available=True)

        else:
            products_list = Product.objects.all().filter(available=True)
        # Calculate discounted price for each product
        for product in products_list:
            product.discounted_price = (product.price * (Decimal(product.discount) / 100))
            product.dis_price = round(product.price-product.discounted_price)
            product.avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']

        paginator=Paginator(products_list,9)
        try:
            page=int(request.GET.get('page','1'))
        except:
            page=1
        try:
            products=paginator.page(page)

        except (EmptyPage,InvalidPage):
            products=paginator.page(paginator.num_pages)
        return render(request, "shopping/category.html", {'category': c_page, 'products': products})


def proDetail(request, c_slug, product_slug):

        try:
            product = Product.objects.get(category__slug=c_slug, slug=product_slug)
            shades = Shades.objects.filter(product=product)
            category_products = Product.objects.filter(category=product.category).exclude(id=product.id)
            review = ProductReview.objects.filter(product=product)
            review_count = review.count()
            average_rating = ProductReview.objects.filter(product=product).aggregate(Avg('rating'))['rating__avg']
            rounded_rating = round(average_rating * 2) / 2
            discount = (product.price * (Decimal(product.discount / 100)))
            discounted_price=round(product.price-discount)

        except Exception as e:
            raise e
        return render(request, "shopping/product.html",
                      {'product': product,
                       'discounted_price':discounted_price,
                       'shades':shades,
                       'review':review,
                       'review_count':review_count,
                       'rounded_rating':rounded_rating,
                       'category_products':category_products,
                      })


def calculate_discounted_price(request):
    # Apply discount logic
    product=Product.objects.all()

    discounted_price = (product.price * (Decimal(product.discount / 100)))
    return render(request, "category.html", {'discounted_price': discounted_price})
