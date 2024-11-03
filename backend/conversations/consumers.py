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
            self.llm = await self.chat_service.init_chat_model(chat)
            await self.accept()
        except Exception as e:
            print(e)
            await self.close()

    async def receive_json(self, content):
        """Handle incoming events

        * Save messages to the database as kind of chat memory, to be able
        to replay the conversation
        * Process messages via chat service
        """
        if content["type"] == "human_message":
            # TODO (not implemented yet)
            # await self.chat_service.save_event(ai_message, type="human_message")
            input_messages = await self.chat_service.collect_context(
                content["data"]["message"]
            )
            ai_message = await self.chat_service.stream_request(
                input_messages, lambda msg: self.send_json(msg)
            )
            await self.send_json({"type": "status", "data": {"ready": 1}})
            # TODO (not implemented yet)
            # await self.chat_service.save_event(ai_message, type="ai_message")
        else:
            await self.send_json({"type": "error", "data": {"message": "Invalid type"}})
