from django.urls import re_path

from conversations.consumers import ChatConsumer


"""
Currently Django-Ninja does not support websocktes. Therefore the configuration for
websockets is done manually. To keep the code clean, the configuration is defined here.
"""
websocket_urlpatterns = [
    re_path(
        r"ws/api/v1/conversations/(?P<conversation_id>[a-zA-Z0-9.-]+)$",
        ChatConsumer.as_asgi(),
    ),
]
