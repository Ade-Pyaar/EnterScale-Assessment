from django.db import models

from core.models import BaseModelClass, Vendor
from core.enum_classes import ProductStatuses


class Product(BaseModelClass):
    owner = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024, null=False, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
        choices=ProductStatuses.choices,
        default=ProductStatuses.IN_STOCK,
    )

    class Meta:
        ordering = ["-created_at"]
