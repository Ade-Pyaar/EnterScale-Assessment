from rest_framework import serializers

from core.util_classes import MyPagination

from vendor.models import Product, ProductStatuses, Vendor


class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["created_by", "last_edited_by", "last_edited_at", "owner"]


class ProductSerializer:

    @staticmethod
    def get_all_products(request):

        product_status = request.query_params.get("status", "All")

        products = Product.objects.filter(owner=request.user.vendor)

        if product_status != "All":
            products = products.filter(status=product_status)

        paginate_data, result, page_error = MyPagination.get_paginated_response(
            queryset=products, request=request
        )

        if page_error:
            return False, None, None

        data = ProductDataSerializer(result, many=True).data

        return True, data, paginate_data

    @staticmethod
    def get_single_product(owner: Vendor, product_id: str, return_data: bool = True):
        try:
            product = Product.objects.filter(id=product_id, owner=owner).first()
        except Exception:
            return None

        if product:
            if return_data:
                data = ProductDataSerializer(product).data
                return data

            return product

        return None

    @staticmethod
    def delete_product(owner, product_id: str):
        try:
            product = Product.objects.filter(id=product_id, owner=owner).first()
        except Exception:
            return False

        if product:
            product.delete()
            return True

        return False


######################################## Add / Edit Product Serializer ##############################################3


class AddProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.FloatField()
    status = serializers.ChoiceField(choices=ProductStatuses.values)

    def validate(self, attrs):
        data = super().validate(attrs)

        owner: Vendor = self.context.get("owner")

        name = data["name"]

        if Product.objects.filter(owner=owner, name=name).exists():
            raise serializers.ValidationError({"name": "A product with this name exists"})

        return data

    def add_product(self):
        owner: Vendor = self.context.get("owner")

        new_product = Product()
        new_product.owner = owner
        new_product.name = self.validated_data["name"]
        new_product.price = self.validated_data["price"]
        new_product.status = self.validated_data["status"]
        new_product.save()

        data = ProductDataSerializer(new_product).data

        return data


class EditProductSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    price = serializers.FloatField(required=False)
    status = serializers.ChoiceField(choices=ProductStatuses.values, required=False)

    def validate(self, attrs):
        data = super().validate(attrs)

        owner: Vendor = self.context.get("owner")
        product: Product = self.context.get("product")

        name = data.get("name")

        if name:
            if Product.objects.filter(owner=owner, name=name).exclude(id=product.id).exists():
                raise serializers.ValidationError({"name": "A product with this name exists"})

        return data

    def edit_product(self):
        product: Product = self.context.get("product")

        product.name = self.validated_data.get("name", product.name)
        product.price = self.validated_data.get("price", product.price)
        product.status = self.validated_data.get("status", product.status)
        product.save()

        data = ProductDataSerializer(product).data

        return data
