from channels.generic.websocket import AsyncJsonWebsocketConsumer

from conversations.services.consumer_service import Consumer, ConsumerService
from conversations.schemas import ChatEventType, ChatMessageType, ChatEvent, ChatMessage


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
        try:
            event = ChatEvent.model_validate(content)
        except Exception as e:
            print(e)
            return

        if event.type == ChatEventType.MESSAGE:
            data = event.data
            match data.message_type:
                case ChatMessageType.HUMAN_MESSAGE:
                    input_messages = await self.chat_service.collect_context(data.message)
                    ai_message = await self.chat_service.stream_request(
                        input_messages,
                        lambda message: self.send_json(
                            ChatEvent(
                                type=ChatEventType.MESSAGE,
                                data=ChatMessage(
                                    message=message,
                                    message_type=ChatMessageType.AI_MESSAGE
                                )
                            ).model_dump()
                        ),
                    )
                    await self.send_json(
                        ChatEvent(
                            type=ChatEventType.STATUS,
                            data=ChatMessage(
                                message=200,
                                message_type=ChatMessageType.AI_MESSAGE
                            )
                        ).model_dump()
                    )
                    # Feature: Save messages to the database here, to be able to replay the conversation
                    # await self.chat_service.save_events([message, ai_message])
                case ChatMessageType.SETTINGS:
                    chat = await self.chat_service.update_model_configuration(data.message)
                    await self.chat_service.init_chat_model(chat)
                    await self.send_json(
                        ChatEvent(
                            type=ChatEventType.STATUS,
                            data=ChatMessage(
                                message=200,
                                message_type=ChatMessageType.SETTINGS
                            )
                        ).model_dump()
                    )
