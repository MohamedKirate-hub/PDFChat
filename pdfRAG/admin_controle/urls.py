from django.urls import path
from admin_controle import views

app_name = "admin_controle"
urlpatterns = [
    path('rag-settings', views.rag_setting, name="rag-settings"),
    path('rag-settings/save', views.rag_control, name="rag-control"),
    path('logs', views.log_info_view, name="logs"),
]
