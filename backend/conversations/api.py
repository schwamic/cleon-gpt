from ninja import Router
from ninja.errors import HttpError
from conversations.schemas import (
    ChatConfigurationOptions,
    ConversationCreate,
    ConversationPublic,
)
from conversations.services.conversations_service import conversationsService


"""Create your Conversations REST routes here.

Keep the routes (controller layer) clean and simple and put 
the business logic into the service layer. Djange Ninja will
automatically generate the OpenAPI schema.
"""


router = Router(
    tags=["Conversations"],
)


@router.post("/", response=ConversationPublic)
def create_conversation(request, payload: ConversationCreate):
    chat = conversationsService.create_conversation(payload)
    return chat


@router.post(":list_configuration_options", response=ChatConfigurationOptions)
def list_configuration_options(request):
    configuration = conversationsService.list_configuration_options()
    return configuration


"""Not Implemented CRUD Routes
 
To keep a clean REST interface, we implement all CRUD routes 
but return a 405 Method Not Allowed error, if not implemented.
"""


@router.get("/{chat_id}")
def get_converstion(request, chat_id: str):
    raise HttpError(405, "Method Not Allowed")


@router.get("/")
def list_converstions(request):
    raise HttpError(405, "Method Not Allowed")


@router.patch("/{chat_id}")
def update_converstion(request, chat_id: str):
    raise HttpError(405, "Method Not Allowed")


@router.put("/{chat_id}")
def replace_converstion(request, chat_id: str):
    raise HttpError(405, "Method Not Allowed")


@router.delete("/{chat_id}")
def delete_converstion(request, chat_id: str):
    raise HttpError(405, "Method Not Allowed")
