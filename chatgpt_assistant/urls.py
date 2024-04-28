
from . import views
from django.urls import path, include


urlpatterns = [
    path("chat/", views.ChatGptAssistantApiView.as_view()),
    
]