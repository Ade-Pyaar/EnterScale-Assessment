from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    # HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView


from drf_yasg.utils import swagger_auto_schema

# from drf_yasg import openapi

from core.enum_classes import APIMessages
from core.util_classes import APIResponses

from customer.serializers.cart_serializers import CustomerCheckoutSerializer, CustomerCartSerializer


class CustomerCheckoutView(APIView):

    @swagger_auto_schema(request_body=CustomerCheckoutSerializer)
    def post(self, request):
        form = CustomerCheckoutSerializer(data=request.data)

        if form.is_valid():
            data = form.checkout()

            return APIResponses.success_response(
                message=APIMessages.CHECKOUT_SUCCESS, status_code=HTTP_201_CREATED, data=data
            )

        return APIResponses.error_response(
            status_code=HTTP_400_BAD_REQUEST, message=APIMessages.FORM_ERROR, errors=form.errors
        )


class CustomerSingleCartView(APIView):

    def get(self, request, cart_id):

        data = CustomerCartSerializer.get_single_cart(cart_id=cart_id)

        if data:
            return APIResponses.success_response(
                message=APIMessages.SUCCESS, status_code=HTTP_200_OK, data=data
            )

        return APIResponses.error_response(
            status_code=HTTP_404_NOT_FOUND, message=APIMessages.CART_NOT_FOUND
        )
