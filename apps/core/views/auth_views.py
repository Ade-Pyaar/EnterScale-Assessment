from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    # HTTP_403_FORBIDDEN,
)
from rest_framework.views import APIView

# from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema


from core.util_classes import APIResponses
from core.enum_classes import APIMessages

from core.serializers.auth_serializers import (
    NormalLoginSerializer,
    NormalSignUpSerializer,
)


class NormalSignUpView(APIView):
    @swagger_auto_schema(request_body=NormalSignUpSerializer)
    def post(self, request, *args, **kwargs):
        form = NormalSignUpSerializer(data=request.data)

        if form.is_valid():
            form.create_account()

            return APIResponses.success_response(
                message=APIMessages.ACCOUNT_CREATED,
                status_code=HTTP_201_CREATED,
            )

        return APIResponses.error_response(
            status_code=HTTP_400_BAD_REQUEST,
            message=APIMessages.FORM_ERROR,
            errors=form.errors,
        )


class NormalLoginView(APIView):
    @swagger_auto_schema(request_body=NormalLoginSerializer)
    def post(self, request, *args, **kwargs):
        form = NormalLoginSerializer(data=request.data)

        if form.is_valid():
            data, error = form.login(request=request)

            if error:
                return APIResponses.error_response(status_code=HTTP_401_UNAUTHORIZED, message=error)

            return APIResponses.success_response(
                message=APIMessages.LOGIN_SUCCESS, status_code=HTTP_200_OK, data=data
            )

        return APIResponses.error_response(
            status_code=HTTP_400_BAD_REQUEST,
            message=APIMessages.FORM_ERROR,
            errors=form.errors,
        )
