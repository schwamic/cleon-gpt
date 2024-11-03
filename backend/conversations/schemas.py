from enum import Enum
from uuid import UUID

from ninja import Field, ModelSchema, Schema

from conversations.models import AIModel


"""Schemas for domain Conversations

Create your schemas for validation and serialization here.
Models are defined in models.py
"""


class Temperature(float, Enum):
    LOW = 0.2
    MEDIUM = 0.7
    HIGH = 0.9


class ChatConfiguration(Schema):
    top_p: float | None = None
    seed: int | None = None
    temperature: Temperature
    model: str = Field(choi="model")


class ConversationCreate(Schema):
    user_id: str
    configuration: ChatConfiguration


class ConversationPublic(Schema):
    chat_id: UUID = Field(alias="id")


class AIModelPublic(ModelSchema):
    class Meta:
        model = AIModel
        exclude = ['id']


class ChatConfigurationOptions(Schema):
    models: list[AIModelPublic]
    temperatures: list[float]
