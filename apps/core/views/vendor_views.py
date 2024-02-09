from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from core.util_classes import APIResponses
from core.enum_classes import APIMessages, AccountStatuses

from core.serializers.vendor_serializers import (
    VendorSerializer,
    UpdateVendorStatusSerializer,
)


class VendorView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    status = openapi.Parameter(
        "status",
        openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        required=False,
        enum=AccountStatuses.values,
        default=AccountStatuses.ACTIVE,
    )

    @swagger_auto_schema(manual_parameters=[status])
    def get(self, request):

        status = request.query_params.get("status", AccountStatuses.ACTIVE)

        if status not in AccountStatuses.values:
            return APIResponses.error_response(
                status_code=HTTP_400_BAD_REQUEST, message=APIMessages.INVALID_QUERY
            )

        data = VendorSerializer.get_all_vendors(status=status)

        return APIResponses.success_response(
            message=APIMessages.SUCCESS,
            status_code=HTTP_200_OK,
            data=data,
        )


class SingleVendorView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, vendor_id):

        data = VendorSerializer.get_single_vendor(vendor_id=vendor_id, return_data=True)

        if data:
            return APIResponses.success_response(
                message=APIMessages.SUCCESS,
                status_code=HTTP_200_OK,
                data=data,
            )

        return APIResponses.error_response(
            status_code=HTTP_404_NOT_FOUND,
            message=APIMessages.VENDOR_NOT_FOUND,
        )

    @swagger_auto_schema(request_body=UpdateVendorStatusSerializer)
    def patch(self, request, vendor_id):

        vendor = VendorSerializer.get_single_vendor(vendor_id=vendor_id, return_data=False)

        if vendor:

            form = UpdateVendorStatusSerializer(data=request.data, context={"vendor": vendor})

            if form.is_valid():
                data, message = form.update_vendor_status()

                return APIResponses.success_response(
                    message=message,
                    status_code=HTTP_200_OK,
                    data=data,
                )

            return APIResponses.error_response(
                status_code=HTTP_400_BAD_REQUEST,
                message=APIMessages.FORM_ERROR,
                errors=form.errors,
            )

        return APIResponses.error_response(
            status_code=HTTP_404_NOT_FOUND,
            message=APIMessages.VENDOR_NOT_FOUND,
        )
