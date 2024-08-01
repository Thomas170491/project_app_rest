from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


@database_sync_to_async
def get_user_and_secret(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        user = User.objects.get(id=user_id)
        return user
    except Exception:
        return AnonymousUser(), None


class UserAuthMiddle(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["query_string"]:
            query_string = scope["query_string"].decode("utf-8")
            token_key = query_string.split("=")[1]
            scope["user"] = await get_user_and_secret(token_key)
        else:
            scope["user"] = AnonymousUser(), None
        return await super().__call__(scope, receive, send)
