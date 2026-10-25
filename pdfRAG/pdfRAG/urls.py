from django.contrib import admin
from django.urls import path, include
from admin_controle.admin import admin_site

urlpatterns = [
    path('admin/', include("admin_controle.urls")),
    path("admin/", admin_site.urls),
    path("account/", include("user_auth.urls")),
    path("files/", include("loading.urls")),
    path('', include('chatbot.urls')),
]
