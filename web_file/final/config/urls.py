from django.contrib import admin
from django.urls import include, path
from django import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('', include('polls.urls')),
    path('admin/', admin.site.urls),
    
]
