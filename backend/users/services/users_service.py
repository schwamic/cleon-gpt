from django.shortcuts import get_object_or_404
from pydantic import UUID4

from users.models import User


class UsersService:
    """Service Layer
    Handels events from Users REST Controller Layer (api.py)
    """

    def get_user(self, user_id: UUID4) -> User:
        user = get_object_or_404(User, id=user_id)
        return user


usersService = UsersService()
