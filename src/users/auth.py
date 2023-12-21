from hashlib import sha256

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpRequest
from itsdangerous.signer import BadSignature, Signer
from ninja.security import HttpBearer

signer = Signer(secret_key=settings.SECRET_KEY, digest_method=sha256)
UserModel = get_user_model()


class AuthBearer(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> User | None:
        try:
            username = signer.unsign(token)
            return UserModel._default_manager.get_by_natural_key(username)
        except (BadSignature, UserModel.DoesNotExist):
            pass
