from uuid import UUID

from django.shortcuts import get_object_or_404

from conversations.models import AIModel, Chat
from conversations.schemas import (
    ChatConfigurationOptions,
    ConversationCreate,
    Temperature,
)
from users.models import User


class ConversationsService:
    """Service Layer 
    Handels events from Conversations REST Controller Layer (api.py)
    """

    def create_conversation(self, payload: ConversationCreate) -> Chat:
        slug_model = payload.configuration.model
        configuration = payload.configuration.model_dump_json(
            exclude={'model'}
        )
        user = get_object_or_404(
            User,
            id=UUID(payload.user_id)
        )
        model = get_object_or_404(
            AIModel,
            slug_name=slug_model
        )
        chat = Chat.objects.create(
            model=model,
            configuration=configuration)
        chat.users.add(user)
        return chat

    def list_configuration_options(self) -> ChatConfigurationOptions:
        models = list(AIModel.objects.all())
        temperatures = [item.value for item in Temperature]
        return ChatConfigurationOptions(
            models=models,
            temperatures=temperatures
        )


conversationsService = ConversationsService()
