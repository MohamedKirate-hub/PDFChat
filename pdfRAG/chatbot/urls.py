from django.urls import path
from chatbot import views

urlpatterns = [
    path('', views.home_view, name="home-view"),
    path('chatbot/', views.chatbot, name='chat-bot'),
]
