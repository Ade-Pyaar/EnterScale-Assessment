from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    # HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.custom_permissions.vendor_permission import IsVendor

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.enum_classes import APIMessages, ProductStatuses
from core.util_classes import APIResponses

from vendor.serializers.product_serializers import (
    AddProductSerializer,
    ProductSerializer,
    EditProductSerializer,
)


class ProductView(APIView):
    permission_classes = [IsAuthenticated, IsVendor]

    status = openapi.Parameter(
        "status",
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=False,
        enum=ProductStatuses.values + ["All"],
        default="All",
    )

    @swagger_auto_schema(manual_parameters=[status])
    def get(self, request):

        status = request.query_params.get("status", "All")

        if status != "All" and status not in ProductStatuses.values:
            return APIResponses.error_response(
                status_code=HTTP_400_BAD_REQUEST, message=APIMessages.INVALID_QUERY
            )

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

    @swagger_auto_schema(request_body=AddProductSerializer)
    def post(self, request):

        form = AddProductSerializer(data=request.data, context={"owner": request.user.vendor})

        if form.is_valid():
            data = form.add_product()

            return APIResponses.success_response(
                message=APIMessages.PRODUCT_CREATED_SUCCESSFULLY,
                status_code=HTTP_201_CREATED,
                data=data,
            )

        return APIResponses.error_response(
            status_code=HTTP_400_BAD_REQUEST,
            message=APIMessages.FORM_ERROR,
            errors=form.errors,
        )


class SingleProductView(APIView):
    permission_classes = [IsAuthenticated, IsVendor]

    def get(self, request, product_id):

        data = ProductSerializer.get_single_product(
            owner=request.user.vendor, product_id=product_id, return_data=True
        )

        if data:
            return APIResponses.success_response(
                message=APIMessages.SUCCESS, status_code=HTTP_200_OK, data=data
            )

        return APIResponses.error_response(
            status_code=HTTP_404_NOT_FOUND, message=APIMessages.PRODUCT_NOT_FOUND
        )

    @swagger_auto_schema(request_body=EditProductSerializer)
    def put(self, request, product_id):

        product = ProductSerializer.get_single_product(
            owner=request.user.vendor, product_id=product_id, return_data=False
        )

        if product:

            form = EditProductSerializer(
                data=request.data, context={"owner": request.user.vendor, "product": product}
            )

            if form.is_valid():
                data = form.edit_product()

                return APIResponses.success_response(
                    message=APIMessages.PRODUCT_UPDATED_SUCCESSFULLY,
                    status_code=HTTP_200_OK,
                    data=data,
                )

            return APIResponses.error_response(
                status_code=HTTP_400_BAD_REQUEST, message=APIMessages.FORM_ERROR, errors=form.errors
            )

        return APIResponses.error_response(
            status_code=HTTP_404_NOT_FOUND, message=APIMessages.PRODUCT_NOT_FOUND
        )

    def delete(self, request, product_id):

        success = ProductSerializer.delete_product(owner=request.user.vendor, product_id=product_id)

        if success:
            return APIResponses.success_response(
                message=APIMessages.PRODUCT_DELETED, status_code=HTTP_200_OK
            )

        return APIResponses.error_response(
            status_code=HTTP_404_NOT_FOUND, message=APIMessages.PRODUCT_NOT_FOUND
        )
