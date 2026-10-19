from django.urls import path
from loading import views

urlpatterns = [
    path('add/', views.upload_files, name="add-file"),
]