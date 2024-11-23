import json
from enum import Enum
from os import getenv
from uuid import UUID

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import FunctionMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI

import conversations.services.ai_metaprompts as metaprompts
from conversations.clients.weatherapi_client import WeatherAPIClient
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


class ChatService:
    """Specialized Service Layer
    Handels Chat Consumer events and interacts with language models and thrid-party APIs
    """

    def __init__(self):
        self.llm = None
        self.chat_id = None
        self.functions = {"get_current_weather": get_current_weather}
        self.system_message = SystemMessage(metaprompts.MARKDOWN_ASSISTANT)
        self.prompt_template = ChatPromptTemplate(
            [self.system_message, MessagesPlaceholder("msgs")]
        )

    @database_sync_to_async
    def get_chat(self, chat_id: str) -> Chat:
        self.chat_id = chat_id
        chat = Chat.objects.get(id=UUID(chat_id))
        return chat

    @sync_to_async
    def init_chat_model(self, chat: Chat) -> BaseChatModel:
        """Factory Method
        Create the correct language model based on the ChatModel
        """
        if chat.model.slug_provider == AIModel.Provider.AZURE_OPEN_AI:
            if isinstance(chat.configuration, str):
                chat.configuration = json.loads(chat.configuration)
            self.llm = AzureChatOpenAI(
                model=chat.model.slug_name,
                temperature=chat.configuration["temperature"],
                api_version=getenv("OPENAI_API_VERSION"),
                api_key=getenv("AZURE_OPENAI_API_KEY"),
                azure_endpoint=getenv("AZURE_OPENAI_ENDPOINT"),
            )
            return self.llm
        else:
            raise Exception("Model not supported")

    @sync_to_async
    def collect_context(self, input: str) -> list:
        """Function Calling
        Processes the input to find out which functions to call and
        returns function results as messages
        """
        llm_with_tools = self.llm.bind_tools([get_current_weather])
        messages = [HumanMessage(input)]
        ai_msg = llm_with_tools.invoke(messages)

        for tool_call in ai_msg.tool_calls:
            selected_tool = self.functions[tool_call["name"].lower()]
            tool_output = selected_tool.invoke(tool_call["args"])
            messages.append(FunctionMessage(tool_output, name=tool_call["name"]))
        return messages

    @sync_to_async
    def stream_request(self, messages: list, callback):
        parser = StrOutputParser()
        chain = self.prompt_template | self.llm | parser
        ai_message = ""
        for chunk in chain.stream({"msgs": messages}):
            async_to_sync(callback)(chunk)
            ai_message = ai_message + chunk
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
        return chat


"""LangChain Tools

Declare tools/functions here.
"""


@tool
def get_current_weather(city) -> str:
    """Calls a weather service and returns current weather data.

    Args:
        city (str): The location to get the weather for

    Returns:
        str: A description of the current weather in the specified city
    """
    client = WeatherAPIClient()
    data = client.get_current_weather(city)
    return str(data)
