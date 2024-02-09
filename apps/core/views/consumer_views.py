from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from core.util_classes import APIResponses
from core.enum_classes import APIMessages

from core.serializers.consumer_serializer import ConsumerSerializer


class ConsumerView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):


        data = ConsumerSerializer.get_all_consumer()

        return APIResponses.success_response(
            message=APIMessages.SUCCESS, status_code=HTTP_200_OK, data=data
        )
