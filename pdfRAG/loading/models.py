from user_auth.models import User
from django.db import models

class LoadFile(models.Model):
    file_path = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)

class LoadingBase(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name="loaded", blank=True)
    files = models.ManyToManyField(LoadFile, related_name="loading_bases")
