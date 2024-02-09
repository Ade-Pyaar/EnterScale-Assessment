import re

from rest_framework import serializers

from django.contrib.auth import get_user_model



USER_MODEL = get_user_model()


def phone_number_serializer_validator(value: str):
    if len(value) != 14:
        raise serializers.ValidationError(
            "Please enter a correct phone number. We only accept international format."
        )

    if not value.replace("+", "").isnumeric():
        raise serializers.ValidationError("Please enter a valid phone number.")


# def phone_number_bool_validator(value: str):
#     if len(value) != 14:
#         return False

#     if not value.replace("+", "").isnumeric():
#         return False

#     return True


# def phone_number_exist_checker(value: str):
#     if not ApilmeUser.objects.filter(phone_number=value).exists():
#         raise serializers.ValidationError("Phone number does not exist.")


# def email_exist_checker(value):
#     if not ApilmeUser.objects.filter(email=value.lower()).exists():
#         raise serializers.ValidationError("This email does not exist.")


def phone_number_not_exist_checker(value: str):
    if USER_MODEL.objects.filter(phone_number=value).exists():
        raise serializers.ValidationError("Phone number already exist.")


def email_not_exist_checker(value):
    if USER_MODEL.objects.filter(email=value.lower()).exists():
        raise serializers.ValidationError("This email already exist.")



# def email_serializer_verification(email):
#     regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

#     if not bool(re.fullmatch(regex, email)):
#         raise serializers.ValidationError("Invalid email address.")


# def email_bool_verification(email):
#     regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

#     if not bool(re.fullmatch(regex, email)):
#         return False

#     return True


def password_validator(value: str):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d!@#$%^&*()\-_=+{};:,<.>?]{8,20}$"

    # compiling regex
    pat = re.compile(reg)

    # searching regex
    mat = re.search(pat, value)
    if not mat:
        raise serializers.ValidationError("Please enter a stronger password.")
