
from django.contrib import admin
from . import views
from django.urls import path



urlpatterns = [
    path('user-profile/', views.UserProfileView.as_view(), name='user-profile')

]



