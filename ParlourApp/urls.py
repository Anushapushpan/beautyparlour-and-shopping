from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.demo, name='demo'),
    # path('', views.activateEmail, name='email'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('user', views.user, name='user'),
    path('logout', views.logout, name='logout'),
    path('cart/logout/', views.logout, name='logout'),
    path('ShoppingApp/shopping/shopping/logout/', views.logout, name='logout'),
    path('appointment', views.appointment, name='appointment'),
    path('appointment_info', views.appointment_info, name='appointment_info'),
    path('accounts/login/login',views.login, name='login'),
    path('accounts/login/register',views.register, name='register'),
    path('Bridal', views.bridal, name='bridal'),
    path('Makeover', views.makeover, name='makeover'),
    path('Skin', views.skin, name='skin'),
    path('Wax', views.wax, name='wax'),
    path('Hair', views.hair, name='hair'),
    path('Nails', views.nails, name='nails'),
    path('gallery', views.gallery, name='gallery'),
    path('contact', views.contact, name='contact'),

    # CRUD OPERATIONS
    path('delete/<str:id>', views.Delete, name='delete'),
    path('<str:id>', views.Update, name='update'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),

    ####reset password urls####
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/login/',views.login, name='login'),



]