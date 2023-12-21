from typing import Tuple, Union

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import IntegrityError
from django.http import HttpRequest
from ninja import Router

from users import schemas
from users.auth import signer

router = Router()


@router.post(
    "/login", response={200: schemas.LoginResponse, 401: schemas.Message}, auth=None
)
def login(
    request: HttpRequest, data: schemas.Login
) -> Union[schemas.LoginResponse, Tuple[int, schemas.Message]]:
    model_backend = ModelBackend()
    user = model_backend.authenticate(request, data.username, data.password)
    if user:
        return schemas.LoginResponse(token=signer.sign(user.username))
    else:
        return 401, schemas.Message(message="Incorrect username or password")


router.post(
    "/signup", response={201: schemas.Message, 400: schemas.Message}, auth=None
)
def signup(request: HttpRequest, data: schemas.SignUp) -> [int, schemas.Message]:
    UserModel = get_user_model()
    try:
        UserModel._default_manager.create_user(
            username=data.username, password=data.password
        )
        return 201, schemas.Message(message="User has been created successfully")
    except IntegrityError:
        return 400, schemas.Message(message="Username is already taken")


@router.get("/", response=list[schemas.User])
def users(request: HttpRequest) -> list[schemas.User]:
    UserModel = get_user_model()
    return [schemas.User(username=u.username) for u in UserModel._default_manager.all()]
