import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse




class User(AbstractUser):
    """Application user"""


class Conversation(models.Model):
    """One chat thread owned by a user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations")
    title = models.CharField(max_length=255, default="New conversation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [models.Index(fields=["user", "-updated_at"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Return the URL of the conversation page."""
        return reverse("chat:conversation_detail", args=[self.pk])


class Message(models.Model):
    """One turn in a conversation, written by the user or the model."""

    class Role(models.TextChoices):
        # Values match the roles the Gemini API expects.
        USER = "user", "You"
        MODEL = "model", "Assistant"

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=Role.choices)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.get_role_display()}: {self.text[:50]}"
