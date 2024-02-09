from rest_framework import serializers

from core.enum_classes import CartStatuses, NotificationTypes
from core.util_classes import NotificationHelper, EmailSender

from customer.models import CartProduct, CustomerCart

from vendor.models import Vendor


class OrderProductDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartProduct
        fields = ["id", "quantity", "unit_price"]

    def to_representation(self, instance: CartProduct):
        data = super().to_representation(instance)

        data["product_name"] = instance.product.first().name
        data["total_price"] = instance.total_price

        return data


class VendorCartDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerCart
        fields = ["id", "address", "city", "phone_number", "status"]

    def to_representation(self, instance: CustomerCart):
        data = super().to_representation(instance)

        data["products"] = OrderProductDetailsSerializer(instance.cart_products, many=True).data

        return data


class VendorOrderSerializer:

    @staticmethod
    def get_all_orders(vendor: Vendor, status: CartStatuses):

        print(status)

        carts = CustomerCart.objects.filter(cart_products__product__owner=vendor)

        if status != "All":

            carts = carts.filter(status=status)

        data = VendorCartDetailsSerializer(carts, many=True).data

        return data

    @staticmethod
    def get_single_order(vendor: Vendor, cart_id: str, return_data: bool = True):

        single_cart = CustomerCart.objects.filter(
            cart_products__product__owner=vendor, status=CartStatuses.PAID, id=cart_id
        ).first()

        if single_cart:
            if return_data:
                data = VendorCartDetailsSerializer(single_cart).data

                return data

            return single_cart

        return None


class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=[CartStatuses.DELIVER_IN_PROGRESS, CartStatuses.DELIVERED]
    )

    def validate(self, attrs):
        data = super().validate(attrs)

        cart: CustomerCart = self.context.get("cart")

        if cart.status == CartStatuses.DELIVERED:
            raise serializers.ValidationError(
                {"status": "Order have been marked as delivered already."}
            )

        return data

    def update_status(self, vendor: Vendor):

        cart: CustomerCart = self.context.get("cart")
        cart.status = self.validated_data["status"]
        cart.save()

        # send email to user concerning the delivery status

        if cart.status == CartStatuses.DELIVERED:
            # TODO add the payment to the vendor's wallet, after removing the company's commission
            pass
            EmailSender.send_order_delivered_email(cart_id=str(cart.id))

        else:
            EmailSender.send_delivery_in_progress_email(cart_id=str(cart.id))

        NotificationHelper.new_notification(
            notification_type=NotificationTypes.ORDER_NOTIFICATION,
            title="Order status update",
            body=f"{vendor.business_name} updated an order status to {cart.status}",
        )

        data = VendorCartDetailsSerializer(cart).data
        return data
