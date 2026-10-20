from django.urls import path
from loading import views

urlpatterns = [
    path('uploaded/', views.availabel_files, name="uploaded-files"),
    path('add/', views.upload_files, name="add-file"),
    path('delete/<str:pk>', views.remove_file, name="delete-file"),
]