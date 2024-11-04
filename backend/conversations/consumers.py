from channels.generic.websocket import AsyncJsonWebsocketConsumer

from conversations.services.consumer_service import ConsumerService, Consumer


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

        * Routes messages to the appropriate service
        * Sends messages to the client (optional)
        """
        match content["type"]:
            case "human_message":
                input_messages = await self.chat_service.collect_context(
                    content["data"]["message"]
                )
                ai_message = await self.chat_service.stream_request(
                    input_messages, lambda msg: self.send_json(msg)
                )
                await self.send_json({"type": "status", "data": {"ready": 1, "eventType": "human_message"}})
                # Feature: Save messages to the database to be able to replay the conversation
                # human_message: content["data"]["message"]
                # await self.chat_service.save_events([human_message, ai_message])
            case "update_settings":
                chat = await self.chat_service.update_model_configuration(content["data"])
                await self.chat_service.init_chat_model(chat)
                await self.send_json({"type": "status", "data": {"ready": 1, "eventType": "update_settings"}})
            case _:
                await self.send_json({"type": "error", "data": {"message": "Invalid type"}})
