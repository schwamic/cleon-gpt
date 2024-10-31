from ninja import NinjaAPI
from conversations.api import router as conversations_router

api_v1 = NinjaAPI(
    version='1.0.0', urls_namespace='public_api', title='Cleon API')

api_v1.add_router("/conversations/", conversations_router)
