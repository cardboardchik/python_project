
from . import views
from django.urls import path, include


urlpatterns = [
    path("category/", views.CategoriesListApiView.as_view()),
    path("item/", views.ItemListApiView.as_view()),
    path("item/<int:id>", views.ItemApiView.as_view()),

]