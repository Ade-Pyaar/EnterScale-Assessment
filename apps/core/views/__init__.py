from django.http import JsonResponse


from rest_framework.status import HTTP_404_NOT_FOUND

from core.enum_classes import APIMessages


def handler404(request, exception):
    return JsonResponse(
        {
            "success": False,
            "message": APIMessages.NOT_FOUND,
        },
        status=HTTP_404_NOT_FOUND,
    )
