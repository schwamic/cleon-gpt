import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from conversations.services.conversations_service import conversationsService


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive_json(self, content):
        data = content.get("data", None)
        print(data)
        await self.send_json({"type": "receive_json", "data": "Hi!"})

        # await channel_layer.group_send(room.channel_name, {
        #     'type': 'chat_message',
        #     'data': {'message': 'from views'}
        #     })

    async def chat_message(self, event):
        await self.send_json({"event": "To the group?!"})
