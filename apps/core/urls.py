from django.urls import path

from core.views.auth_views import NormalLoginView, NormalSignUpView
from core.views.vendor_views import VendorView, SingleVendorView
from core.views.consumer_views import ConsumerView
from core.views.notification_views import NotificationView

urlpatterns = [
    ################ auth views
    path("auth/login/", NormalLoginView.as_view(), name="login-view"),
    path("auth/sign-up/", NormalSignUpView.as_view(), name="signup-view"),
    ################ vendor views
    path("vendors/", VendorView.as_view(), name="vendor-view"),
    path("vendors/<str:vendor_id>/", SingleVendorView.as_view(), name="single-vendor-view"),
    ################ vendor views
    path("consumers/", ConsumerView.as_view(), name="consumer-view"),
    ################ notification views
    path("notifications/", NotificationView.as_view(), name="notification-view"),
]
