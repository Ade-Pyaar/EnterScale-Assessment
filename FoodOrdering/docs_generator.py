from django.conf import settings

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

from rest_framework.permissions import AllowAny


class VendorAPISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.base_path = "/api/v1/vendor/"

        if settings.DEBUG:
            schema.schemes = ["http"]
        else:
            schema.schemes = ["https"]

        return schema


class CustomerAPISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.base_path = "/api/v1/customer/"

        if settings.DEBUG:
            schema.schemes = ["http"]
        else:
            schema.schemes = ["https"]

        return schema


class CoreAPISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.base_path = "/api/v1/core/"

        if settings.DEBUG:
            schema.schemes = ["http"]
        else:
            schema.schemes = ["https"]
        return schema


core_schema_view = get_schema_view(
    openapi.Info(
        title="Food Ordering Core API Documentation",
        default_version="v1",
        description="API documentation for core operations",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="Adebayoibrahim2468@gmail.com"),
        license=openapi.License(name="Leemao"),
    ),
    public=True,
    permission_classes=[AllowAny],
    urlconf="apps.core.urls",
    generator_class=CoreAPISchemeGenerator,
)

vendor_schema_view = get_schema_view(
    openapi.Info(
        title="Food Ordering Vendor API Documentation",
        default_version="v1",
        description="API documentation for vendor operations",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="Adebayoibrahim2468@gmail.com"),
        license=openapi.License(name="Leemao"),
    ),
    public=True,
    permission_classes=[AllowAny],
    urlconf="apps.vendor.urls",
    generator_class=VendorAPISchemeGenerator,
)

customer_schema_view = get_schema_view(
    openapi.Info(
        title="Food Ordering Customer API Documentation",
        default_version="v1",
        description="API documentation for customer operations",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="Adebayoibrahim2468@gmail.com"),
        license=openapi.License(name="Leemao"),
    ),
    public=True,
    permission_classes=[AllowAny],
    urlconf="apps.customer.urls",
    generator_class=CustomerAPISchemeGenerator,
)
