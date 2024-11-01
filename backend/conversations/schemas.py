from ninja import Schema, Field
from uuid import UUID
from enum import Enum


class Temperature(float, Enum):
    LOW = 0.2
    MEDIUM = 0.7
    HIGH = 0.9


class ChatConfiguration(Schema):
    top_p: float | None = None
    seed: int | None = None
    temperature: Temperature


class ConversationCreate(Schema):
    user_id: str
    configuration: ChatConfiguration
    model: str


class ConversationPublic(Schema):
    chat_id: UUID = Field(alias="id")
