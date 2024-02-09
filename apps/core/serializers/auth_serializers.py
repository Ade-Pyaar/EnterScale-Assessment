from django.contrib.auth import authenticate

from rest_framework import serializers

from core.models import CustomUser, Vendor
from core.enum_classes import AccountTypes, APIMessages, AccountStatuses
from core.api_authentication import MyAPIAuthentication
from core.validators import (
    email_not_exist_checker,
    phone_number_not_exist_checker,
    phone_number_serializer_validator,
    password_validator,
)


################################################ Sign Up / Login Serializer ###########################################


class NormalSignUpSerializer(serializers.Serializer):
    email_address = serializers.EmailField(validators=[email_not_exist_checker])
    phone_number = serializers.CharField(
        validators=[phone_number_not_exist_checker, phone_number_serializer_validator]
    )
    password = serializers.CharField(validators=[password_validator])
    business_name = serializers.CharField()
    address = serializers.CharField()
    state = serializers.CharField()
    brief_description = serializers.CharField()

    def create_account(self):
        # create a user account

        new_user = CustomUser()
        new_user.email = self.validated_data["email_address"].lower()
        new_user.phone_number = self.validated_data["phone_number"]
        new_user.set_password(self.validated_data["password"])
        new_user.account_status = AccountStatuses.WAITING_APPROVAL
        new_user.account_type = AccountTypes.VENDOR
        new_user.save()

        new_vendor = Vendor()
        new_vendor.user_account = new_user
        new_vendor.business_name = self.validated_data["business_name"].title()
        new_vendor.address = self.validated_data["address"]
        new_vendor.state = self.validated_data["state"]
        new_vendor.brief_description = self.validated_data["brief_description"]
        new_vendor.save()


class NormalLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def login(self, request):
        email: str = self.validated_data["email"].lower()
        password = self.validated_data["password"]

        user: CustomUser = authenticate(request, username=email, password=password)

        if user:

            if user.account_status == AccountStatuses.DEACTIVATED:
                return None, APIMessages.ACCOUNT_DEACTIVATED

            if user.account_status == AccountStatuses.INACTIVE:
                return None, APIMessages.ACCOUNT_BLOCKED

            if user.account_status == AccountStatuses.WAITING_APPROVAL:
                return None, APIMessages.ACCOUNT_NOT_APPROVED

            # login successful
            auth_token, auth_exp = MyAPIAuthentication.get_access_token(
                {
                    "user_id": str(user.id),
                }
            )

            data = {
                "auth_token": auth_token,
                "auth_token_exp": auth_exp,
                "refresh_token": MyAPIAuthentication.get_refresh_token(),
                "account_type": user.account_type,
            }

            return data, None

        return None, APIMessages.LOGIN_FAILURE
