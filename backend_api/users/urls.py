from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.CustomLoginView.as_view(), name="login")
]



