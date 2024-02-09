from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings

from core.enum_classes import AccountStatuses

user_model = get_user_model()


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        user = user_model.objects.filter(email=username.lower()).first()

        if user:
            # Check if password is correct or user is already deactivated
            if user.check_password(password):  # or user.status == AccountStatuses.INACTIVE:
                if user.login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                    self.deactivate_user(user)
                else:
                    self.reset_login_attempts(user)

                return user

            self.increment_login_attempts(user)
            return None

        return None

    def deactivate_user(self, user):
        user.status = AccountStatuses.INACTIVE
        user.save()

    def reset_login_attempts(self, user):
        user.login_attempts = 0
        user.save()

    def increment_login_attempts(self, user):
        user.login_attempts += 1
        user.save()
