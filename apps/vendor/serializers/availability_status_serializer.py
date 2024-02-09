from rest_framework import serializers

from core.enum_classes import StoreStatuses, APIMessages, NotificationTypes
from core.util_classes import NotificationHelper

from vendor.models import Vendor


class UpdateAvailabilityStatus(serializers.Serializer):
    status = serializers.ChoiceField(choices=StoreStatuses.choices)

    def update_status(self, vendor: Vendor):

        status = self.validated_data["status"]
        vendor.availability = status
        vendor.save()

        NotificationHelper.new_notification(
            notification_type=NotificationTypes.VENDOR_NOTIFICATION,
            title="Availability Status Updated",
            body=f"{vendor.business_name} updated their availability status to {status}",
        )

        if status == StoreStatuses.OPEN:
            return APIMessages.STORE_OPENED

        return APIMessages.STORE_CLOSED
