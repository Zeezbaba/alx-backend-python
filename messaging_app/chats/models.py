from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)

class Conversation(models.Model):
    """conversation model"""
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_names='conversation')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"conversation {self.id}"

class Message(models.Model):
    """ message model """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} in conversation {self.conversation.id}"
