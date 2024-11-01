from uuid import UUID

from django.shortcuts import get_object_or_404

from users.models import User


"""
Service Layer for Controller Layer (api.py)
"""


class UsersService:
    def get_user(self, user_id: str) -> User:
        user = get_object_or_404(User, id=UUID(user_id))
        return user


usersService = UsersService()
