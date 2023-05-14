from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name='ShoppingApp'
urlpatterns = [
    path('shopping/shopping/', views.allProdCat, name='allProdCat'),
    path('<slug:c_slug>/', views.allProdCat, name='products_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/', views.proDetail, name='prodCatdetail'),
    path('category/<int:id>/', views.proDetail, name='proDetail'),
    path('category/<slug:c_slug>/<slug:product_slug>/', views.proDetail, name='proDetail'),

    ]