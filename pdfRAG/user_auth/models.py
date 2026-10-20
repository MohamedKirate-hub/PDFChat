from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL,
                             null=True,
                             related_name="users")
