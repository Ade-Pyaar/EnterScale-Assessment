from django.contrib import admin
from django.urls import path, include


from .docs_generator import (
    core_schema_view,
    vendor_schema_view, customer_schema_view
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/core/", include("apps.core.urls")),
    path("api/v1/customer/", include("apps.customer.urls")),
    path("api/v1/vendor/", include("apps.vendor.urls")),
    
    # documentation paths
    path(
        "docs/core/",
        core_schema_view.with_ui("swagger", cache_timeout=0),
        name="core-swagger-ui",
    ),
    path(
        "docs/vendor/",
        vendor_schema_view.with_ui("swagger", cache_timeout=0),
        name="vendor-swagger-ui",
    ),
    path(
        "docs/customer/",
        customer_schema_view.with_ui("swagger", cache_timeout=0),
        name="customer-swagger-ui",
    ),

]


handler404 = "apps.core.views.handler404"
