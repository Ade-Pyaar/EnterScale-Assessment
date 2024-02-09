from django.db import models


from core.models import BaseModelClass
from core.enum_classes import TransactionStatuses, CartStatuses


class Consumer(BaseModelClass):
    email = models.EmailField(max_length=1024, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)


class CustomerCart(BaseModelClass):
    consumer = models.ForeignKey(Consumer, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=1024, null=False, blank=False)
    address = models.CharField(max_length=1024, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(max_length=1024, null=True, blank=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
        choices=CartStatuses.choices,
        default=CartStatuses.PENDING,
    )
    code = models.CharField(max_length=1024, null=True, blank=True)


class CartProduct(BaseModelClass):
    product = models.ManyToManyField("vendor.Product")
    quantity = models.IntegerField(null=True, blank=True)
    unit_price = models.IntegerField(null=True, blank=True)
    cart = models.ForeignKey(CustomerCart, on_delete=models.CASCADE, related_name="cart_products")

    @property
    def total_price(self):
        return self.quantity * self.unit_price


class CustomerTransaction(BaseModelClass):

    cart = models.ForeignKey(CustomerCart, on_delete=models.SET_NULL, null=True, blank=True)

    reference = models.CharField(max_length=3096, null=True, blank=True)
    provider_reference = models.CharField(max_length=3096, null=True, blank=True)

    payable_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    source_account_number = models.CharField(max_length=1024, null=True, blank=True)
    source_account_name = models.CharField(max_length=1024, null=True, blank=True)
    source_bank_name = models.CharField(max_length=1024, null=True, blank=True)

    transaction_date = models.DateTimeField(null=True, blank=True)

    narration = models.TextField(null=True, blank=True)

    transaction_status = models.CharField(max_length=30, choices=TransactionStatuses.choices)

    meta_data = models.JSONField(default=dict, null=True, blank=True)
