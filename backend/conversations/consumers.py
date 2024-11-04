from enum import Enum

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from conversations.services.consumer_service import Consumer, ConsumerService


class ChatEventType(str, Enum):
    STATUS = "status"
    MESSAGE = "message"


class ChatMessageType(str, Enum):
    HUMAN_MESSAGE = "human_message"
    AI_MESSAGE = "ai_message"
    SETTINGS = "update_settings"


"""Consumers are WebSocket controllers that handle events.

Currently Django Ninja does not support WebSockets and does not automatically
generate OpenAPI schema for WebSockets.

"""


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """Specialized Consumer
    Controlles Chat event flow
    """

    async def connect(self):
        """Handle connection
        Currently no authentication is implemented yet.
        """
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        try:
            self.chat_service = ConsumerService.create_service_by_type(
                Consumer.CHAT)
            chat = await self.chat_service.get_chat(self.conversation_id)
            await self.chat_service.init_chat_model(chat)
            await self.accept()
        except Exception as e:
            print(e)
            await self.close()

    async def receive_json(self, content):
        """Handle incoming events

        * Routes messages to appropriate services
        * Sends messages to clients
        """
        if content["type"] == ChatEventType.MESSAGE:
            message = content["data"]["message"]
            match content["data"]["message_type"]:
                case ChatMessageType.HUMAN_MESSAGE:
                    input_messages = await self.chat_service.collect_context(
                        content["data"]["message"]
                    )
                    ai_message = await self.chat_service.stream_request(
                        input_messages, lambda message: self.send_json({
                            "type": ChatEventType.MESSAGE,
                            "data": {"message": message, "message_type": ChatMessageType.AI_MESSAGE}
                        })
                    )
                    await self.send_json({"type": ChatEventType.STATUS, "data": {"code": 200, "message_type": ChatMessageType.HUMAN_MESSAGE}})
                    # Feature: Save messages to the database here, to be able to replay the conversation
                    # await self.chat_service.save_events([message, ai_message])
                case ChatMessageType.SETTINGS:
                    chat = await self.chat_service.update_model_configuration(message)
                    await self.chat_service.init_chat_model(chat)
                    await self.send_json({"type": ChatEventType.STATUS, "data": {"code": 200, "message_type": ChatMessageType.SETTINGS}})
                case _:
                    await self.send_json({"type": ChatEventType.STATUS, "data": {"code": 400}})
