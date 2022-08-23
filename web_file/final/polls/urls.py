from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    
    path('',views.first),
    path('submit/',views.submit),
    path('submit2/',views.submit),
    path('margin/',views.margin),
    path('polls/',views.test),
    
   
]