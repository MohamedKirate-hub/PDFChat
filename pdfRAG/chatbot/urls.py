from django.urls import path
from chatbot import views

urlpatterns = [
    # path('test/', views.see_files, name='see-files'),
    path('', views.home_view, name="home-view"),
    path('chatbot/', views.chatbot, name='chat-bot'),
]
