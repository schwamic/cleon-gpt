from ninja import Router
from ninja.errors import HttpError

from users.schemas import UserPublic
from users.services.users_service import usersService


router = Router(
    tags=["Users"],
)


@router.get("/{user_id}", response=UserPublic)
def get_user(request, user_id: str):
    user = usersService.get_user(user_id)
    return user


"""
Not Implemented CRUD Routes
"""


@router.get("/")
def list_users(request):
    raise HttpError(405, "Method Not Allowed")


@router.post("/")
def create_user(request):
    raise HttpError(405, "Method Not Allowed")


@router.patch("/{user_id}")
def update_user(request, user_id: str):
    raise HttpError(405, "Method Not Allowed")


@router.put("/{user_id}")
def replace_user(request, user_id: str):
    raise HttpError(405, "Method Not Allowed")


@router.delete("/{user_id}")
def delete_user(request, user_id: str):
    raise HttpError(405, "Method Not Allowed")
