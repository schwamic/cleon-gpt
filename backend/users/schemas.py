from ninja import ModelSchema

from users.models import User


"""Schemas for domain Users

Create your schemas for validation and serialization here.
Models are defined in models.py
"""


class UserPublic(ModelSchema):
    class Meta:
        model = User
        fields = ["id", "nickname"]
