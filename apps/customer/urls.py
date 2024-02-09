from django.urls import path

from customer.views.cart_views import CustomerCheckoutView, CustomerSingleCartView
from customer.views.product_views import ProductView

urlpatterns = [
    path("cart/<str:card_id>/", CustomerSingleCartView.as_view(), name="customer-single-cart-view"),
    path("checkout/", CustomerCheckoutView.as_view(), name="customer-checkout-view"),
    path("products/", ProductView.as_view(), name="customer-product-view"),
]
