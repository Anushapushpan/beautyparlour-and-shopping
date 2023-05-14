from django.urls import path
from  . import views

app_name = 'TryonApp'
urlpatterns = [
    path('TryonApp',views.tryon,name='TryonApp'),
]