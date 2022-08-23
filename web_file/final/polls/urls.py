from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    
    path('',views.main_page),
    path('submit/',views.submit),
    path('submit2/',views.submit),
    path('margin/',views.margin),
    path('polls/',views.test),
    
   
]