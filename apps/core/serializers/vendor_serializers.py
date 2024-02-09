from rest_framework import serializers

from core.models import Vendor
from core.enum_classes import AccountStatuses, APIMessages


class VendorDetailsSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user_account.email")
    phone_number = serializers.EmailField(source="user_account.phone_number")
    account_status = serializers.EmailField(source="user_account.account_status")

    class Meta:
        model = Vendor
        fields = [
            "id",
            "business_name",
            "email",
            "phone_number",
            "account_status",
            "address",
            "state",
            "brief_description",
            "availability",
            "created_at",
        ]


class VendorSerializer:

    @staticmethod
    def get_all_vendors(status: AccountStatuses):

        vendors = Vendor.objects.filter(user_account__account_status=status)

        data = VendorDetailsSerializer(vendors, many=True).data
        return data


    @staticmethod
    def get_single_vendor(vendor_id: str, return_data: bool = True):

        try:
            vendor = Vendor.objects.filter(id=vendor_id).first()

        except Exception:
            return None

        if vendor:
            if return_data:
                data = VendorDetailsSerializer(vendor).data
                return data

            return vendor

        return None


class UpdateVendorStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[AccountStatuses.ACTIVE, AccountStatuses.DEACTIVATED])

    def validate(self, attrs):
        data = super().validate(attrs)

        status = data.get("status")

        vendor: Vendor = self.context.get("vendor")

        if status == vendor.user_account.account_status:
            raise serializers.ValidationError({"status": f"Vendor is already in {status} state."})

        return data

    def update_vendor_status(self):

        vendor: Vendor = self.context.get("vendor")
        status = self.validated_data["status"]

        vendor.user_account.account_status = status
        vendor.user_account.save()
        vendor.save()

        data = VendorDetailsSerializer(vendor).data

        if status == AccountStatuses.DEACTIVATED:
            message = APIMessages.VENDOR_DEACTIVATED

        else:
            message = APIMessages.VENDOR_ACTIVATED

        return data, message
