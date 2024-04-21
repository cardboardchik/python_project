
from . import views
from django.urls import path, include


urlpatterns = [
    path("category/all", views.CategoriesListApiView.as_view()),
    path("category/create", views.CategoriesCreateApiView.as_view())
]




