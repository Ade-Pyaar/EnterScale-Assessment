from rest_framework.permissions import BasePermission


class IsVendor(BasePermission):
    """
    Allows access only to vendor account.
    """

    def has_permission(self, request, view):
        return request.user is not None and bool(request.user.vendor)
