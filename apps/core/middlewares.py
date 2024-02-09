import logging

import traceback

from django.http import JsonResponse

from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR


logger = logging.getLogger("server_error")


class Log500ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(
            "\n".join(
                traceback.format_exception(type(exception), exception, exception.__traceback__)
            )
        )

        return JsonResponse(
            {
                "message": "An error has occurred but don't worry. We will worry about it",
            },
            status=HTTP_500_INTERNAL_SERVER_ERROR,
        )
