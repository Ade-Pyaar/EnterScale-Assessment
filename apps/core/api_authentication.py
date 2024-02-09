from random import choices
from datetime import timedelta
import string
import uuid
import jwt

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions


from core.enum_classes import AccountStatuses


user_model = get_user_model()

class MyAPIAuthentication(BaseAuthentication):
    def authenticate(self, request):
        data = self.validate_request(request.headers)
        if not data:
            return None, None

        return self.get_user(data["user_id"]), None

    def get_user(self, user_id):
        try:
            user_id = uuid.UUID(user_id)
            user = (
                user_model.objects.filter(id=user_id)
                .filter(account_status=AccountStatuses.ACTIVE)
                .first()
            )
            return user
        except Exception:
            return None

    def validate_request(self, headers):
        authorization = headers.get("Authorization", None)

        if not authorization:
            return None

        token_header = authorization.split(" ")
        if len(token_header) == 2:
            header = token_header[0]
            if header == "Bearer":
                token = token_header[1]

                decoded_data = self.verify_token(token)

                if decoded_data:
                    return decoded_data

                raise exceptions.AuthenticationFailed(_("Invalid or Expired token."))

            raise exceptions.AuthenticationFailed(
                _("Invalid token header. No credentials provided.")
            )

        raise exceptions.AuthenticationFailed(_("Invalid token header. No credentials provided."))

    @staticmethod
    def verify_token(token):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

        except Exception:
            return None

        exp = decoded["exp"]

        if timezone.now().timestamp() > exp:
            return None

        return decoded

    @classmethod
    def get_random_token(cls, length):
        """generates token"""
        return "".join(choices(string.ascii_uppercase + string.digits, k=length))

    @classmethod
    def get_access_token(cls, payload):
        return jwt.encode(
            {"exp": timezone.now() + timedelta(days=30), **payload},
            settings.SECRET_KEY,
            algorithm="HS256",
        ), timezone.now() + timedelta(days=30)

    @classmethod
    def get_refresh_token(cls):
        return jwt.encode(
            {
                "exp": timezone.now() + timedelta(days=365),
                "data": cls.get_random_token(15),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
