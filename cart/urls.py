from django.urls import path
from  . import views


app_name='cart'
urlpatterns=[
    path('add/<int:product_id>/',views.add_cart,name='add_cart'),
    path('',views.cart_detail,name='cart_detail'),
    # path('tryon',views.tryon,name='tryon'),
    # path('tryon_pink',views.tryon_pink,name='tryon_pink'),
    # path('tryon_red',views.tryon_red,name='tryon_red'),
    # path('tryon_nude_pink', views.tryon_nude_pink, name='tryon_nude_pink'),
    # # path('cart/',views.cart,name='cart'),
    path('remove/<int:product_id>/',views.cart_remove,name='cart_remove'),
    path('full_remove/<int:product_id>/', views.full_remove, name='full_remove'),
    path('checkout',views.checkout,name='checkout'),
    path('place-order',views.placeorder,name='placeorder'),
    path('proceed-to-pay',views.razorpaycheck,name='razorpaycheck'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('view-order/<str:t_no>',views.orderview,name='orderview'),
    path('track_order/',views.track_order,name='track_order'),
    path('cart/payment-receipt/<str:payment_id>/', views.generate_payment_receipt, name='payment_receipt'),
    path('review/',views.Review_rate,name='Review_rate'),
    path('success/<str:razorpay_payment_id>/', views.success, name='success'),


    # path('proceed-to-pay',views.razorpaycheck,name=razorpaycheck),

]