from user_auth.models import User
from django.db import models

class LoadFile(models.Model):
    file_path = models.FilePathField()

class LoadingBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="loaded", blank=True)
    files = models.ManyToManyField(LoadFile)
