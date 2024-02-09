import decimal

from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from django.utils import timezone


from core.enum_classes import APIMessages, TransactionStatuses, CartStatuses, NotificationTypes
from core.util_classes import (
    APIResponses,
    DeliveryTimeHelper,
    NotificationHelper,
    EmailSender,
    PeriodicTaskHelper,
)


from customer.models import CustomerTransaction


class PayStackCallback(APIView):
    """Callback for paystack"""

    swagger_schema = None

    def post(self, request, *args, **kwargs):
        response: dict = request.data

        if response["event"] == "charge.success":
            # the transaction is successful
            transaction_data: dict = response["data"]

            transaction_reference = transaction_data["reference"]
            provider_reference = transaction_data["id"]
            status = transaction_data["status"]

            amount = float(transaction_data["amount"]) / 100

            # maybe useful later
            _ = transaction_data["channel"]

            transaction_object = CustomerTransaction.objects.filter(
                reference=transaction_reference
            ).first()

            if transaction_object is None:
                # invalid transaction reference
                return APIResponses.success_response(
                    message=APIMessages.TRANSACTION_NOT_FOUND,
                    status_code=HTTP_200_OK,
                )

            if transaction_object.transaction_status in [
                TransactionStatuses.SUCCESS,
                TransactionStatuses.FAILED,
            ]:
                return APIResponses.success_response(
                    message=APIMessages.TRANSACTION_COMPLETED_ALREADY,
                    status_code=HTTP_200_OK,
                )

            if status == "success":
                # update the transaction object
                transaction_object.transaction_status = TransactionStatuses.SUCCESS
                transaction_object.last_edited_at = timezone.now()
                transaction_object.paid_amount = decimal.Decimal(amount)
                transaction_object.provider_reference = provider_reference

                transaction_object.cart.delivery_time = DeliveryTimeHelper.get_delivery_time()
                transaction_object.cart.status = CartStatuses.PAID
                transaction_object.save()

                # set the task that will send email 30 minutes before the delivery time

                PeriodicTaskHelper.create_30_minutes_delivery_task(
                    cart_id=str(transaction_object.cart.id),
                    delivery_time=transaction_object.cart.delivery_time,
                )

                # send email notification to the customer
                # send email notification to the admin
                # send notification to the vendor concerning order details
                EmailSender.send_order_placed_email(
                    cart_id=str(transaction_object.cart.id),
                    vendor_email=transaction_object.cart.cart_products.first()
                    .product.first()
                    .owner.user_account.email,
                    business_name=transaction_object.cart.cart_products.first()
                    .product.first()
                    .owner.user_account.email,
                )

                NotificationHelper.new_notification(
                    notification_type=NotificationTypes.ORDER_NOTIFICATION,
                    title="Order Placed",
                    body=f"{transaction_object.cart.email or transaction_object.cart.phone} has placed an order.",
                )

                return APIResponses.success_response(
                    message=APIMessages.TRANSACTION_SUCCESSFUL,
                    status_code=HTTP_200_OK,
                )

        if response["event"] == "charge.failed":
            # effect the change and send the required notification
            # update the transaction object
            transaction_object.transaction_status = TransactionStatuses.FAILED
            transaction_object.last_edited_at = timezone.now()

            transaction_object.provider_reference = provider_reference
            transaction_object.save()

            return APIResponses.success_response(
                message=APIMessages.TRANSACTION_FAILED,
                status_code=HTTP_200_OK,
            )

        if response["event"] == "charge.reversed":
            # effect the change and send the required notification

            # update the transaction object
            transaction_object.transaction_status = TransactionStatuses.FAILED
            transaction_object.last_edited_at = timezone.now()

            transaction_object.provider_reference = provider_reference
            transaction_object.save()

            return APIResponses.success_response(
                message=APIMessages.TRANSACTION_FAILED,
                status_code=HTTP_200_OK,
            )

        return APIResponses.success_response(
            message=APIMessages.SUCCESS,
            status_code=HTTP_200_OK,
        )
