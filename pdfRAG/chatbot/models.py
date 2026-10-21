from django.db import models
from user_auth.models import User

class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# class Conversation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.ForeignKey(Message)
#     created_at = models.DateTimeField(auto_now_add=True)

class Conversation(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    conversations = models.ManyToManyField(Message)
    created_at = models.DateTimeField(auto_now_add=True)
