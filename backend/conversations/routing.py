from django.urls import re_path

from conversations.consumers import ChatConsumer


""" WebSocket URL configuration

Currently Django-Ninja does not support websocktes;
therefore the configuration for websockets is done manually.
"""
websocket_urlpatterns = [
    re_path(
        r"ws/api/v1/conversations/(?P<conversation_id>[a-zA-Z0-9.-]+)$",
        ChatConsumer.as_asgi(),
    ),
]
