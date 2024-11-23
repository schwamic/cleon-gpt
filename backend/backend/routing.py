"""
ROUTING configuration for backend project.

For more information please see:
    https://test-channels.readthedocs.io/en/latest/getting-started.html#routing
"""
from django.urls import re_path

from conversations.consumers import ChatConsumer


""" 
WS(s) Channels API
"""
websocket_urlpatterns = [
    re_path(
        r"api/v1/conversations/(?P<conversation_id>[a-zA-Z0-9.-]+)$",
        ChatConsumer.as_asgi(),
    ),
]


"""
AsyncAPI documentation for Websocket connections.
"""
asyncapi_v3_json_schema = {
    "asyncapi": "3.0.0",
    "info": {
        "title": "Cleon AsyncAPI",
        "version": "0.1.1",
        "description": "Cleon AsyncAPI documentation for Websocket connections. See http://localhost:8000/api/v1/docs/openapi/v3 for OpenAPI REST documentation."
    },
    "defaultContentType": "application/json",
    "servers": {
        "ws-connections": {
            "host": "127.0.0.1:8000/api",
            "protocol": "ws"
        }
    },
    "channels": {
        "chat": {
            "address": "v1/conversations/{conversation_id}",
            "messages": {
                "ChatMessage": {
                    "$ref": "#/components/messages/ChatMessage"
                },
                "ChatMessageReply": {
                    "$ref": "#/components/messages/ChatMessageReply"
                }
            }
        }
    },
    "operations": {
        "sendChatEvent": {
            "action": "send",
            "description": "What a user can send to the server.",
            "channel": {
                "$ref": "#/channels/chat"
            },
            "messages": [
                {
                    "$ref": "#/channels/chat/messages/ChatMessage"
                }
            ],
            "reply": {
                "messages": [
                    {
                        "$ref": "#/channels/chat/messages/ChatMessageReply"
                    }
                ],
                "channel": {
                    "$ref": "#/channels/chat"
                }
            }
        }
    },
    "components": {
        "messages": {
            "ChatMessage": {
                "name": "Prompt",
                "title": "User Messages",
                "contentType": "application/json",
                "payload": {
                    "$ref": "#/components/schemas/ChatMessage"
                }
            },
            "ChatMessageReply": {
                "name": "Prompt",
                "title": "Server Messages",
                "contentType": "application/json",
                "payload": {
                    "$ref": "#/components/schemas/ChatMessageReply"
                }
            }
        },
        "schemas": {
            "ChatMessage": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "const": "message"
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "message_type": {
                                "type": "string",
                                "enum": [
                                    "human_message",
                                    "update_settings"
                                ]
                            },
                            "message": {
                                "oneOf": [
                                    {
                                        "type": "string"
                                    },
                                    {
                                        "type": "object",
                                        "properties": {
                                            "model": {
                                                "type": "string"
                                            },
                                            "temperature": {
                                                "type": "number",
                                                "enum": [0.2, 0.7, 0.9]
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            "ChatMessageReply": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["message", "status"]
                    },
                    "data": {
                        "type": "object",
                        "properties": {
                            "message_type": {
                                "type": "string",
                                "enum": [
                                    "ai_message",
                                    "update_settings"
                                ]
                            },
                            "message": {
                                "oneOf": [
                                    {
                                        "type": "string"
                                    },
                                    {
                                        "type": "object",
                                        "properties": {
                                            "model": {
                                                "type": "string"
                                            },
                                            "temperature": {
                                                "type": "number",
                                                "enum": [0.2, 0.7, 0.9]
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }
        }
    }
}
