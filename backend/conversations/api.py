from ninja import Router
from ninja.errors import HttpError
from conversations.schemas import ConversationCreate, ConversationPublic
from conversations.services.conversations_service import conversationsService

router = Router(
    tags=["Conversations"],
)


@router.post("/", response=ConversationPublic)
def create_conversation(request, payload: ConversationCreate):
    chat = conversationsService.create_conversation(payload)
    return chat


"""
Not Implemented CRUD Routes
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
