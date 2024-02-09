from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.enum_classes import APIMessages, CartStatuses
from core.util_classes import APIResponses
from core.custom_permissions.vendor_permission import IsVendor

from vendor.serializers.order_serializers import VendorOrderSerializer, UpdateOrderStatusSerializer


class VendorOrderView(APIView):
    permission_classes = [IsAuthenticated, IsVendor]

    status = openapi.Parameter(
        "status",
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=False,
        enum=CartStatuses.values + ["All"],
        default="All",
    )

    @swagger_auto_schema(manual_parameters=[status])
    def get(self, request):

        status = request.query_params.get("status", "All")

        if status != "All" and status not in CartStatuses.values:
            return APIResponses.error_response(
                status_code=HTTP_400_BAD_REQUEST, message=APIMessages.INVALID_QUERY
            )

        data = VendorOrderSerializer.get_all_orders(vendor=request.user.vendor, status=status)

        return APIResponses.success_response(
            message=APIMessages.SUCCESS, status_code=HTTP_200_OK, data=data
        )


class SingleOrderProductView(APIView):
    permission_classes = [IsAuthenticated, IsVendor]

    def get(self, request, cart_id):

        data = VendorOrderSerializer.get_single_order(
            vendor=request.user.vendor, cart_id=cart_id, return_data=True
        )

        if data:
            return APIResponses.success_response(
                message=APIMessages.SUCCESS, status_code=HTTP_200_OK, data=data
            )

        return APIResponses.error_response(
            status_code=HTTP_404_NOT_FOUND, message=APIMessages.ORDER_NOT_FOUND
        )

    @swagger_auto_schema(request_body=UpdateOrderStatusSerializer)
    def patch(self, request, cart_id):

        cart = VendorOrderSerializer.get_single_order(
            vendor=request.user.vendor, cart_id=cart_id, return_data=False
        )

        if cart:

            form = UpdateOrderStatusSerializer(data=request.data, context={"cart": cart})

            if form.is_valid():
                data = form.update_status(vendor=request.user.vendor)

                return APIResponses.success_response(
                    message=APIMessages.SUCCESS, status_code=HTTP_200_OK, data=data
                )

            return APIResponses.error_response(
                status_code=HTTP_400_BAD_REQUEST, message=APIMessages.FORM_ERROR, errors=form.errors
            )

        return APIResponses.error_response(
            status_code=HTTP_404_NOT_FOUND, message=APIMessages.ORDER_NOT_FOUND
        )
