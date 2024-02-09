from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,

    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.enum_classes import APIMessages
from core.util_classes import APIResponses
from customer.serializers.product_serializers import ProductSerializer


class ProductView(APIView):


    search_query = openapi.Parameter(
        "search_query",
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=False,
    )

    @swagger_auto_schema(manual_parameters=[search_query])
    def get(self, request):
        success, data, paginate_data = ProductSerializer.get_all_products(request=request)

        if success:
            return APIResponses.success_response(
                message=APIMessages.SUCCESS,
                status_code=HTTP_200_OK,
                data=data,
                paginate_data=paginate_data,
            )

        return APIResponses.error_response(
            status_code=HTTP_400_BAD_REQUEST, message=APIMessages.PAGINATION_PAGE_ERROR
        )


class SingleProductView(APIView):


    def get(self, request, product_id):

        data = ProductSerializer.get_single_product(product_id=product_id)

        if data:
            return APIResponses.success_response(
                message=APIMessages.SUCCESS, status_code=HTTP_200_OK, data=data
            )

        return APIResponses.error_response(
            status_code=HTTP_404_NOT_FOUND, message=APIMessages.PRODUCT_NOT_FOUND
        )
