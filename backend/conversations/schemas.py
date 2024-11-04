from enum import Enum
from uuid import UUID

from ninja import Field, ModelSchema, Schema

from conversations.models import AIModel, Chat


"""Schemas for domain Conversations

Create your schemas for validation and serialization here.
Models are defined in models.py
"""


class Temperature(float, Enum):
    LOW = 0.2
    MEDIUM = 0.7
    HIGH = 0.9


class CreateChatConfiguration(Schema):
    temperature: Temperature
    model: str


class ConversationCreate(Schema):
    user_id: str
    configuration: CreateChatConfiguration


class ConversationPublic(Schema):
    chat_id: UUID = Field(alias="id")


class AIModelPublic(ModelSchema):
    class Meta:
        model = AIModel
        exclude = ["id"]


class ChatConfigurationOptions(Schema):
    models: list[AIModelPublic]
    temperatures: list[float]


class ChatPublic(ModelSchema):
    model: AIModelPublic

    class Meta:
        model = Chat
        exclude = ["id", "users"]
