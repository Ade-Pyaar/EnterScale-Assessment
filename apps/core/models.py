import uuid

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from core.enum_classes import AccountTypes, AccountStatuses, StoreStatuses, NotificationTypes


class BaseModelClass(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    created_by = models.CharField(max_length=1024, null=True, blank=True)
    last_edited_by = models.CharField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser, BaseModelClass):
    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS = ["username"]

    # overriding username field so as to make it optional
    username = models.CharField(max_length=64, null=True, blank=True, default=None, unique=False)
    name = models.CharField(max_length=2048, null=True, blank=True)

    email = models.EmailField(max_length=1024, null=True, blank=True, unique=True, db_index=True)
    phone_number = models.CharField(
        max_length=15, null=True, blank=True, unique=True, db_index=True
    )
    password = models.CharField(max_length=2048, null=False, blank=False, editable=False)

    account_type = models.CharField(
        max_length=1024, blank=True, null=True, choices=AccountTypes.choices
    )

    account_status = models.CharField(
        max_length=1024, null=True, blank=False, choices=AccountStatuses.choices
    )

    login_attempts = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.account_type)


class Vendor(BaseModelClass):
    user_account = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=1024, null=False, blank=False, unique=True)
    address = models.CharField(max_length=1024, null=False, blank=False, unique=True)
    state = models.CharField(max_length=1024, null=False, blank=False, unique=True)

    brief_description = models.CharField(max_length=1024, null=True, blank=True)

    availability = models.CharField(
        max_length=1024,
        null=False,
        blank=False,
        choices=StoreStatuses.choices,
        default=StoreStatuses.OPEN,
    )



class Notification(BaseModelClass):
    title = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    notification_type = models.CharField(
        max_length=1024, null=False, choices=NotificationTypes.choices
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title}"
