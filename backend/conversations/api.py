from ninja import Router

router = Router(
    tags=["Conversations"],
)


@router.get('/{conversation_id}")')
def get_conversation(request, conversation_id: str):
    return [{"conversation": conversation_id}]


# TODO ALL CRUD OPERATIONS
