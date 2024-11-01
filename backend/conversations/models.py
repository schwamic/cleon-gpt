import uuid

from django.db import models

from users.models import User


class AIModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    # TODO: slug = models.CharField(max_length=100, unique=True)
    endpoint = models.URLField()
    api_key_name = models.CharField(max_length=50, null=True, blank=True)


class AIFunction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    # TODO: slug = models.CharField(max_length=100, unique=True)
    endpoint = models.URLField()
    api_key_name = models.CharField(max_length=50, null=True, blank=True)


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, null=True, blank=True)
    model = models.ForeignKey(
        AIModel, on_delete=models.SET_NULL, null=True, blank=True)
    configuration = models.JSONField()


class ChatEvents(models.Model):
    class ChatEventType(models.TextChoices):
        HUMAN_MESSAGE = "human_message"
        AI_MESSAGE = "ai_message"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    type = models.CharField(choices=ChatEventType.choices, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
