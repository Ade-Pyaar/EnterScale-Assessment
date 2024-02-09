from rest_framework import serializers


from core.enum_classes import ProductStatuses
from core.util_classes import PaymentProviderHelper, CodeGenerator

from vendor.models import Product

from customer.models import (
    CustomerCart,
    CartProduct,
    CustomerTransaction,
    TransactionStatuses,
    Consumer,
)


class CustomerCartDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCart
        fields = [""]


class CustomerCartSerializer:

    @staticmethod
    def get_single_cart(cart_id: str):
        try:
            cart = CustomerCart.objects.filter(id=cart_id).first()
        except Exception:
            return None

        if cart:
            data = CustomerCartDataSerializer(cart).data
            return data

        return None


class CheckoutProductSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField()

    def validate(self, attrs):
        data = super().validate(attrs)

        product_id = data.get("product_id")

        product = Product.objects.filter(id=product_id, status=ProductStatuses.IN_STOCK).first()

        if product is None:
            raise serializers.ValidationError(
                {"product_id": "Product does not exist or is out of stock."}
            )

        data["product"] = product

        return data


class CustomerCheckoutSerializer(serializers.Serializer):
    products = serializers.ListField(child=CheckoutProductSerializer(), allow_empty=False)
    address = serializers.CharField()
    city = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()

    def checkout(self):

        consumer, _ = Consumer.objects.get_or_create(
            email=self.validated_data.get("email"),
            phone_number=self.validated_data.get("phone_number"),
        )

        new_cart = CustomerCart()
        new_cart.consumer = consumer
        new_cart.address = self.validated_data["address"]
        new_cart.city = self.validated_data["city"]
        new_cart.phone_number = self.validated_data["phone_number"]
        new_cart.email = self.validated_data.get("email")
        new_cart.code = CodeGenerator.generate_order_code()
        new_cart.save()

        # create the cart products

        total_price = 0

        for product_entry in self.validated_data["products"]:
            new_cart_product = CartProduct()
            new_cart_product.quantity = product_entry["quantity"]
            new_cart_product.unit_price = product_entry["product"].price
            new_cart_product.cart = new_cart
            new_cart_product.save()
            new_cart_product.product.add(product_entry["product"])
            new_cart_product.save()

            total_price += new_cart_product.total_price

        # create a new transaction object
        new_transaction = CustomerTransaction()
        new_transaction.cart = new_cart
        new_transaction.reference = CodeGenerator.generate_transaction_reference()
        new_transaction.narration = f"Cart Payment by {new_cart.email}, with id {new_cart.id}"
        new_transaction.transaction_status = TransactionStatuses.PENDING
        new_transaction.payable_amount = total_price
        new_transaction.save()

        # get the payment link from here
        payment_link = PaymentProviderHelper.generate_paystack_payment_link(
            amount=float(total_price), email=new_cart.email, reference=new_transaction.reference
        )

        data = {"payment_link": payment_link}

        return data
