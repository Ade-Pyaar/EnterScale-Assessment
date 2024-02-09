from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from core.enum_classes import APIMessages
from core.util_classes import APIResponses
from core.custom_permissions.vendor_permission import IsVendor

from vendor.serializers.availability_status_serializer import UpdateAvailabilityStatus


class AvailabilityStatusView(APIView):
    permission_classes = [IsAuthenticated, IsVendor]

    @swagger_auto_schema(request_body=UpdateAvailabilityStatus)
    def patch(self, request):

        form = UpdateAvailabilityStatus(data=request.data)

        if form.is_valid():
            message = form.update_status(vendor=request.user.vendor)

            return APIResponses.success_response(message=message, status_code=HTTP_200_OK)

        return APIResponses.error_response(
            status_code=HTTP_400_BAD_REQUEST, message=APIMessages.FORM_ERROR, errors=form.errors
        )
