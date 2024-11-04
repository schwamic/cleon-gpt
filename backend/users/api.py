from ninja import Router
from ninja.errors import HttpError
from pydantic import UUID4

from users.schemas import UserPublic
from users.services.users_service import usersService

"""Create your Users REST routes here.

Keep the routes (controller layer) clean and simple and put 
the business logic into the service layer. Djange Ninja will
automatically generate the OpenAPI schema.
"""


router = Router(
    tags=["Users"],
)


@router.get("/{user_id}", response=UserPublic)
def get_user(request, user_id: UUID4):
    user = usersService.get_user(user_id)
    return user


"""Not Implemented CRUD Routes
 
To keep a clean REST interface, we implement all CRUD routes 
but return a 405 Method Not Allowed error, if not implemented.
"""


@router.get("/")
def list_users(request):
    raise HttpError(405, "Method Not Allowed")


@router.post("/")
def create_user(request):
    raise HttpError(405, "Method Not Allowed")


@router.patch("/{user_id}")
def update_user(request, user_id: UUID4):
    raise HttpError(405, "Method Not Allowed")


@router.put("/{user_id}")
def replace_user(request, user_id: UUID4):
    raise HttpError(405, "Method Not Allowed")


@router.delete("/{user_id}")
def delete_user(request, user_id: UUID4):
    raise HttpError(405, "Method Not Allowed")
