from ninja import ModelSchema

from users.models import User


class UserPublic(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'nickname']
