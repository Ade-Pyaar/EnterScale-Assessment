from random import choices
import string

# from io import BytesIO
# import imghdr
# import base64

# import math
import json

# import logging
from datetime import timedelta, datetime


# from dateutil.relativedelta import relativedelta

import requests


# import pendulum

from django.core.paginator import Paginator
from django.conf import settings

from django_celery_beat.models import PeriodicTask, CrontabSchedule

from rest_framework.response import Response

from core.enum_classes import NotificationTypes

from core.models import Notification

from core.tasks import (
    send_order_placed_email,
    send_order_delivered_email,
    send_delivery_in_progress_email,
    send_30_minutes_to_delivery_email,
)


def snake_case_to_camel_case(value: str):
    splitted_string = value.split("_")

    camel_string = splitted_string.pop(0)

    for other_words in splitted_string:
        camel_string += other_words.title()

    return camel_string


class APIResponses:
    @classmethod
    def success_response(cls, message: str, status_code, data=None, paginate_data=None):
        context = {
            "message": message,
        }

        if data is not None:
            context["data"] = data

            if paginate_data:
                context["pagination"] = paginate_data

        return Response(context, status=status_code)

    @classmethod
    def error_response(cls, status_code, message, errors: dict = None):
        context = {
            "message": message,
        }

        if errors is not None:
            errors_list = []
            for key, value in errors.items():
                if isinstance(value, list):
                    value = value[0]

                key = snake_case_to_camel_case(key)

                errors_list.append({"fieldName": key, "error": value})

            context["errors"] = errors_list

        return Response(context, status=status_code)

    @classmethod
    def server_error(cls, message: str, status_code):
        context = {"message": message}

        return Response(context, status=status_code)


class MyPagination:
    @classmethod
    def get_paginated_response(
        cls, request, queryset, page_size_param="page_size", page_number_param="page"
    ):
        page_number = request.query_params.get(page_number_param, 1)
        page_size = request.query_params.get(page_size_param, 25)

        paginator = Paginator(queryset, page_size)
        try:
            current_page = paginator.page(page_number)
        except Exception:
            return None, None, "Invalid page number"

        total_data = {
            "currentPage": current_page.number,
            "numberOfPages": paginator.num_pages,
            "nextPage": current_page.next_page_number() if current_page.has_next() else None,
            "previousPage": (
                current_page.previous_page_number() if current_page.has_previous() else None
            ),
        }

        return total_data, current_page.object_list, None


class CodeGenerator:

    @staticmethod
    def generate_transaction_reference():
        upper = choices(string.ascii_uppercase, k=7)
        digits = choices(string.digits, k=7)
        total = upper + digits

        return "".join(total)

    @staticmethod
    def generate_order_code():
        upper = choices(string.ascii_uppercase, k=3)
        digits = choices(string.digits, k=4)
        total = upper + digits

        return "".join(total)


class DeliveryTimeHelper:

    @staticmethod
    def get_delivery_time():

        # Get the current time
        current_time = datetime.now()

        # Add one hour to the current time
        delivery_time = current_time + timedelta(hours=1)

        remaining_minutes = 60 - delivery_time.minute

        delivery_time += timedelta(minutes=remaining_minutes)

        delivery_time.replace(second=0, microsecond=0)

        return delivery_time


class NotificationHelper:
    @staticmethod
    def new_notification(
        notification_type: NotificationTypes,
        title: str = None,
        body: str = None,
    ):
        new_history = Notification()
        new_history.notification_type = notification_type
        new_history.title = title
        new_history.body = body
        new_history.save()

        # create_activity_history.delay(creator_id=creator_id, name=name)


class PaymentProviderHelper:
    @staticmethod
    def generate_paystack_payment_link(amount: float, email: str, reference: str):
        url = "https://api.paystack.co/transaction/initialize"

        payload = {
            "amount": amount * 100,
            "email": email,
            "reference": reference,
        }

        headers = {
            "authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "content-type": "application/json",
        }

        response = requests.post(
            url=url,
            data=json.dumps(payload),
            headers=headers,
            timeout=120,
        )

        response_json: dict = response.json()

        if response_json["status"] is True:
            return response_json["data"]["authorization_url"]

        print(f"Unable to generate paystack payment link: {response_json}")
        return None


# class ActivityHistoryHelper:
#     @staticmethod
#     def new_activity_history(creator_id: str, name: str, item_id: str = None):
#         if settings.ENVIRONMENT == "production":
#             create_activity_history.delay(creator_id=creator_id, name=name, item_id=item_id)
#         else:
#             create_activity_history(creator_id=creator_id, name=name, item_id=item_id)


class EmailSender:
    @staticmethod
    def send_order_placed_email(cart_id: str, vendor_email: str, business_name):
        if settings.ENVIRONMENT == "production":
            send_order_placed_email.delay(
                cart_id=cart_id, vendor_email=vendor_email, business_name=business_name
            )
        else:
            send_order_placed_email(
                cart_id=cart_id, vendor_email=vendor_email, business_name=business_name
            )

    @staticmethod
    def send_order_delivered_email(cart_id: str):
        if settings.ENVIRONMENT == "production":
            send_order_delivered_email.delay(cart_id=cart_id)
        else:
            send_order_delivered_email(cart_id=cart_id)

    @staticmethod
    def send_delivery_in_progress_email(cart_id: str):
        if settings.ENVIRONMENT == "production":
            send_delivery_in_progress_email.delay(cart_id=cart_id)
        else:
            send_delivery_in_progress_email(cart_id=cart_id)

    @staticmethod
    def send_30_minutes_to_delivery_email(cart_id: str):
        if settings.ENVIRONMENT == "production":
            send_30_minutes_to_delivery_email.delay(cart_id=cart_id)
        else:
            send_30_minutes_to_delivery_email(cart_id=cart_id)


class PeriodicTaskHelper:

    @staticmethod
    def create_30_minutes_delivery_task(cart_id: str, delivery_time):

        email_time: datetime = delivery_time - timedelta(minutes=30)

        schedule = CrontabSchedule()
        schedule.minute = email_time.minute
        schedule.hour = email_time.hour
        schedule.day_of_month = email_time.day
        schedule.month_of_year = email_time.month
        schedule.save()

        new_task = PeriodicTask()
        new_task.crontab = schedule
        new_task.one_off = True
        new_task.enabled = True
        new_task.name = f"30 minutes before delivery for {cart_id}"
        new_task.task = "core.tasks.send_30_minutes_to_delivery_email"
        new_task.args = json.dumps([str(cart_id)])

        new_task.save()


# class WalletHelper:
#     @staticmethod
#     def create_wallet(organization: Organization):
#         if settings.ENVIRONMENT == "production":
#             # only do this in production

#             wallet = Wallet()
#             wallet.owner = organization
#             wallet.description = f"Wallet for {organization.name or organization.id}"
#             wallet.save()

#             create_virtual_wallet.delay(wallet_id=str(wallet.id))
