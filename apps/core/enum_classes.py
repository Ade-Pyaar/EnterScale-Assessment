from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class AccountStatuses(TextChoices):
    ACTIVE = "Active", _("Active")
    INACTIVE = "Inactive", _("Inactive")
    DEACTIVATED = "Deactivated", _("Deactivated")
    WAITING_APPROVAL = "Waiting Approval", _("Waiting Approval")

class NotificationTypes(TextChoices):
    ORDER_NOTIFICATION = "Order Notification", _("Order Notification")
    VENDOR_NOTIFICATION = "Vendor Notification", _("Vendor Notification")

class AccountTypes(TextChoices):
    VENDOR = "Vendor", _("Vendor")
    ADMIN = "Admin", _("Admin")


class StoreStatuses(TextChoices):
    OPEN = "Open", _("Open")
    CLOSED = "Closed", _("Closed")

class CartStatuses(TextChoices):
    PENDING = "Pending", _("Pending")
    PAID = "Paid", _("Paid")
    DELIVER_IN_PROGRESS = "Delivery in progress", _("Delivery in progress")
    DELIVERED = "Delivered", _("Delivered")


class ProductStatuses(TextChoices):
    IN_STOCK = "In Stock", _("In Stock")
    OUT_OF_STOCK = "Out of Stock", _("Out of Stock")


class TransactionStatuses(TextChoices):
    PENDING = "Pending", _("Pending")
    SUCCESS = "Success", _("Success")
    FAILED = "Failed", _("Failed")
    IN_PROGRESS = "In Progress", _("In Progress")


class TransactionTypes(TextChoices):
    DEBIT = "DEBIT", _("DEBIT")



class NotificationTitles:
    ORDER_PLACED = "Order Placed"
    ORDER_DELIVERED = "Order Delivered"
    ORDER_CANCELLED = "Order Cancelled"
    ORDER_REJECTED = "Order Rejected"
    



class APIMessages:
    WELCOME_MESSAGE_TITLE = "Welcome to Stock Keeper"
    WELCOME_MESSAGE_BODY = """
Welcome to Stock Keeper! We are thrilled to have you join our community. Get ready to unlock a world of possibilities with our app, designed to enhance your inventory management. Feel free to explore our features, and should you need any assistance, our dedicated support team is here to help. Thank you for choosing Stock Keeper, and we look forward to providing you with an exceptional experience.
Best regards, CEO."""

    SUCCESS = "Operation completed successfully"
    FORM_ERROR = "One or more validation(s) failed"
    ACCOUNT_CREATED = "Account created successfully, please wait a for some time while we approve your account. You will receive an email when your account is approved."
    ACCOUNT_SETUP_NOT_COMPLETED = "Account setup not completed"
    ACCOUNT_SETUP_COMPLETED = "Account setup completed"
    ACCOUNT_SETUP_COMPLETED_ALREADY = "Account setup completed already"
    ACCOUNT_DEACTIVATED = (
        "Your account has been deactivated, please reach out to your organization admin"
    )
    ACCOUNT_BLOCKED = "Your account has been blocked, please reset your password to activate it"
    ACCOUNT_NOT_APPROVED = "Your account has not been approved, please wait a while for approval"

    FEEDBACK_MESSAGE = "Your message has been received"

    OTP_SENT = "OTP sent successfully"
    OTP_VERIFIED = "OTP verified successfully"

    PASSWORD_CHANGED = "Password changed successfully"
    PASSWORD_RESET = "Password reset successfully"
    PASSWORD_RESET_LOGGED_IN_ERROR = "You cannot reset password while logged in."
    PASSWORD_RESET_CODE_SENT = "Password reset code sent successfully."
    PASSWORD_RESET_CODE_VERIFIED = "Code verified successfully."
    PASSWORD_CREATE_SUCCESS = "Password created successfully."

    LOGIN_SUCCESS = "Login successful"
    LOGIN_FAILURE = "Invalid login credentials"
    ACCOUNT_LOCKED = (
        "Your account has been locked, please reset your password to unlock your account."
    )

    ACCOUNT_DELETED = "Account deleted successfully"

    INVITE_SUCCESS = "User invited successfully"

    TOKEN_REFRESH_FAILURE = "Invalid or expired token"

    PROFILE_UPDATED_SUCCESSFULLY = "Profile Updated"

    FORBIDDEN = "Access denied"
    NOT_FOUND = "Page not found."

    PAGINATION_PAGE_ERROR = "Page not found"

    # Query parameter errors
    INVALID_STATUS = "Invalid Status"
    INVALID_ITEM_TYPE = "Invalid Item Type"
    INVALID_QUERY = "Invalid query"

    # product message
    PRODUCT_CREATED_SUCCESSFULLY = "Product created successfully"
    PRODUCT_UPDATED_SUCCESSFULLY = "Product updated successfully"
    PRODUCT_CLONED_SUCCESSFULLY = "Product cloned successfully"
    PRODUCT_DELETED = "Product deleted successfully"
    PRODUCT_NOT_FOUND = "Product not found"

    # export messages
    INVALID_EXPORT_FILE_TYPE = "Invalid export file type"
    EXPORT_FILE_TYPE_NEEDED = "Export file type is needed"

    PLEASE_COMPLETE_PAYMENT = "You can now proceed to make the payment"

    # transaction messages
    TRANSACTION_COMPLETED_ALREADY = "Transaction completed already"
    TRANSACTION_NOT_FOUND = "Transaction not found"
    TRANSACTION_SUCCESSFUL = "Transaction Successful"
    TRANSACTION_FAILED = "Transaction Failed"
    TRANSACTION_INITIALIZED = "Transaction initiated successfully"

    CHECKOUT_SUCCESS = "Checkout Successful"

    CART_NOT_FOUND = "Cart not found"
    ORDER_NOT_FOUND = "Order not found"

    STORE_OPENED = "Store opened"
    STORE_CLOSED = "Store closed"


    VENDOR_ACTIVATED = "Vendor activated"
    VENDOR_DEACTIVATED = "Vendor deactivated"
    VENDOR_NOT_FOUND = "Vendor not found"