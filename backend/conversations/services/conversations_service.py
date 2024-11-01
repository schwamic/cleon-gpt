from uuid import UUID

from django.shortcuts import get_object_or_404

from conversations.models import Chat, AIModel
from conversations.schemas import ConversationCreate
from users.models import User

"""
Service Layer for Controller Layer (api.py)
"""


class ConversationsService:
    def create_conversation(self, payload: ConversationCreate) -> Chat:
        user = get_object_or_404(User, id=UUID(payload.user_id))
        model = get_object_or_404(AIModel, name=payload.model)
        chat = Chat.objects.create(
            model=model,
            configuration=payload.configuration.model_dump_json()
        )
        chat.users.add(user)
        return chat


conversationsService = ConversationsService()
