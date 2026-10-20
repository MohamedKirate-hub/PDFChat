from django.urls import path
from chatbot import views

urlpatterns = [
    path('test/', views.see_files, name='see-files'),
]
