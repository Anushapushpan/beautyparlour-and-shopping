from django.urls import path
from  . import views

app_name='Search_App'
urlpatterns=[
    path('',views.SearchResult,name='SearchResult'),
]