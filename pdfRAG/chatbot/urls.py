from django.urls import path
from chatbot import views

urlpatterns = [
    path('', views.home_view, name="home-view"),
    path('chatbot', views.converstaions_view, name="conversations"),
    path('chatbot/create', views.create_conversation, name='create-conversation'),
    path('chatbot/<str:pk>/delete', views.delete_conversation, name="delete-conversation"),
    path('chatbot/<str:pk>/conversation', views.chatbot, name='conversation-chat'),
]
