import json
from enum import Enum
from os import getenv
from uuid import UUID

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from langchain_core.messages import HumanMessage
from langchain_openai import AzureChatOpenAI

from agents.workflows.tools_markdown_chatbot import Node, ToolsMarkdownWorkflow
from conversations.models import AIModel, Chat
from conversations.schemas import UpdateChatConfiguration


class Consumer(str, Enum):
    CHAT = "chat"


class Configuration(str, Enum):
    MODEL = "model"
    TEMPERATURE = "temperature"


class ConsumerService:
    """Service Layer
    Handels WebSocket Controller Layer events (consumers.py)
    """

    @staticmethod
    def create_service_by_type(consumer_type: str):
        """Factory Methodet
        Create the correct service based on the consumer type"""
        if consumer_type == Consumer.CHAT:
            return ChatService()
        else:
            raise Exception("Consumer not supported")


class ChatService:
    """Specialized Service Layer
    Handels Chat Consumer events and interacts with language models and thrid-party APIs
    """

    def __init__(self):
        self.chat_id = None
        self.agent = None
        self.config = None

    @database_sync_to_async
    def get_chat(self, chat_id: str) -> Chat:
        self.chat_id = chat_id
        chat = Chat.objects.get(id=UUID(chat_id))
        self.config = {"configurable": {"thread_id": chat_id}}
        return chat

    # TODO
    # * Add last chat state if available
    @sync_to_async
    def init_chat_model(self, chat: Chat) -> None:
        """Factory Method
        Create the correct language model based on the chat object
        """
        if chat.model.slug_provider == AIModel.Provider.AZURE_OPEN_AI:
            if isinstance(chat.configuration, str):
                chat.configuration = json.loads(chat.configuration)
            llm = AzureChatOpenAI(
                model=chat.model.slug_name,
                temperature=chat.configuration["temperature"],
                api_version=getenv("OPENAI_API_VERSION"),
                api_key=getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
            )
            self.agent = ToolsMarkdownWorkflow(llm).graph
        else:
            raise Exception("Provider not supported")

    @sync_to_async
    def stream_request(self, user_prompt: str, callback) -> str:
        """Stream outputs from the final node
        Filter by custom tag "result_node", to stream only values from the result_model
        """
        ai_message = ""
        for msg, metadata in self.agent.stream({"messages": [HumanMessage(user_prompt)]}, stream_mode="messages", config=self.config):
            if (
                msg.content
                and not isinstance(msg, HumanMessage)
                and metadata["langgraph_node"] == Node.ASSISTANT
            ):
                async_to_sync(callback)(msg.content)
                ai_message = ai_message + msg.content
        return ai_message

    @database_sync_to_async
    def update_model_configuration(self, payload: UpdateChatConfiguration) -> Chat:
        chat = Chat.objects.get(id=UUID(self.chat_id))
        if payload.model is not None:
            ai_model = AIModel.objects.get(slug_name=payload.model)
            chat.model = ai_model
        if payload.temperature is not None:
            chat.configuration = {"temperature": payload.temperature.value}
        chat.save()
        # TODO
        # Run init_chat_model again, this sould not be done by the consumer
        return chat
