import uuid

from django.db import models

from users.models import User


""" Models for domain Conversations

Create your Database Tables here. Schemas are defined in schemas.py
"""


class AIModel(models.Model):
    class Provider(models.TextChoices):
        AZURE_OPEN_AI = "azure-openai"

    class Name(models.TextChoices):
        GPT_4O = "gpt-4o"
        GPT_4O_MINI = "gpt-4o-mini"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    slug_name = models.CharField(
        choices=Name.choices, max_length=50, unique=True)
    provider = models.CharField(max_length=50)
    slug_provider = models.CharField(
        choices=Provider.choices, max_length=50)


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, null=True, blank=True)
    model = models.ForeignKey(
        AIModel, on_delete=models.SET_NULL, null=True, blank=True)
    configuration = models.JSONField()


class ChatEvents(models.Model):
    class Type(models.TextChoices):
        HUMAN_MESSAGE = "human_message"
        AI_MESSAGE = "ai_message"
        FUNCTION_MESSAGE = "function_message"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    type = models.CharField(choices=Type.choices, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
