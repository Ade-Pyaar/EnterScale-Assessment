from rest_framework import serializers

from core.util_classes import MyPagination
from core.enum_classes import StoreStatuses

from vendor.models import Product, ProductStatuses


class ProductDataSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source="owner.business_name")

    class Meta:
        model = Product
        exclude = ["created_by", "last_edited_by", "last_edited_at", "owner"]


class ProductSerializer:

    @staticmethod
    def get_all_products(request):

        search_query = request.query_params.get("search_query", None)

        products = Product.objects.filter(
            status=ProductStatuses.IN_STOCK, owner__availability=StoreStatuses.OPEN
        )

        if search_query:
            products = products.filter(name__icontains=search_query)

        paginate_data, result, page_error = MyPagination.get_paginated_response(
            queryset=products, request=request
        )

        if page_error:
            return False, None, None

        data = ProductDataSerializer(result, many=True).data

        return True, data, paginate_data

    @staticmethod
    def get_single_product(product_id: str):
        try:
            product = Product.objects.filter(id=product_id).first()
        except Exception:
            return None

        if product:

            data = ProductDataSerializer(product).data
            return data

        return None
