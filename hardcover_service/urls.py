"""
URL configuration for hardcover_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from hardcover_backend.views import insert_book_by_isbn
urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include("polls.urls")),
    path('api/insert-book', insert_book_by_isbn, name="get-object"),
    path('api-auth/', include('rest_framework.urls')),
]
