from ninja import Schema


class Message(Schema):
    message: str


class Login(Schema):
    username: str
    password: str


class LoginResponse(Schema):
    token: str


class SignUp(Schema):
    username: str
    password: str


class User(Schema):
    username: str
