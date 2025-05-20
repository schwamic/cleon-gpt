import uuid

from django.db import models

from users.models import User


""" Models for domain Conversations

Create your Database Tables here. Schemas are defined in schemas.py
"""


class AIModel(models.Model):
    class Provider(models.TextChoices):
        AZURE_OPEN_AI = "azure-openai"
        OPEN_AI = "openai"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    slug_name = models.CharField(max_length=50, unique=True)
    provider = models.CharField(max_length=50)
    slug_provider = models.CharField(choices=Provider.choices, max_length=50)


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, blank=True)
    model = models.ForeignKey(
        AIModel, on_delete=models.SET_NULL, null=True, blank=True)
    configuration = models.JSONField()
