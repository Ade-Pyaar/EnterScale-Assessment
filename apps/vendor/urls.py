from django.urls import path

from vendor.views.product_views import ProductView, SingleProductView
from vendor.views.order_views import VendorOrderView, SingleOrderProductView
from vendor.views.availability_status_views import AvailabilityStatusView

urlpatterns = [
    path("products/", ProductView.as_view(), name="vendor-product-view"),
    path("products/<str:product_id>/", SingleProductView.as_view(), name="vendor-single-product-view"),

    ################# orders
    path("orders/", VendorOrderView.as_view(), name="vendor-order-view"),
    path("orders/<str:cart_id>/", SingleOrderProductView.as_view(), name="vendor-single-order-view"),
    
    
    ################# availability
    path("availability/", AvailabilityStatusView.as_view(), name="vendor-availability-status-view"),


]