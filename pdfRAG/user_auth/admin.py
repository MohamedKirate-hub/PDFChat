from django.contrib import admin
from user_auth.models import User, UserRole

admin.site.register(UserRole)
admin.site.register(User)
