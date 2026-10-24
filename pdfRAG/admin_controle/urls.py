from django.urls import path
from admin_controle import views

app_name = "admin_controle"
urlpatterns = [
    path('admin/rag-settings', views.rag_setting, name="rag-settings"),
    path('admin/rag-settings/save', views.rag_control, name="rag-control"),
]
