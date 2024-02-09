import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from celery import shared_task


from django.conf import settings

from customer.models import CustomerCart


@shared_task(bind=True)
def send_order_placed_email(self, cart_id: str, vendor_email: str, business_name: str):

    try:

        customer_cart = CustomerCart.objects.filter(id=cart_id).first()

        total_price = 0

        product_details = ""

        for product in customer_cart.cart_products.all():

            product_details += f"<p>{product.product.first().name} x {product.quantity} units @ ₦ {product.unit_price} each</p>"

            total_price += product.total_price

        with open("emails/order_placed_email_customer.html") as f:
            customer_template = f.read()

        customer_template = customer_template.replace("#order_code", customer_cart.code)
        customer_template = customer_template.replace(
            "#shipping_address", f"{customer_cart.address}, {customer_cart.city}"
        )
        customer_template = customer_template.replace(
            "#total_price", "₦ " + str(float(total_price))
        )
        customer_template = customer_template.replace("#product_details", product_details)
        customer_template = customer_template.replace(
            "#delivery_time", customer_cart.delivery_time.strftime("%b %d, %Y %I:%M %p")
        )

        with open("emails/order_placed_email_vendor.html") as f:
            vendor_template = f.read()

        vendor_template = vendor_template.replace("#business_name", business_name)
        vendor_template = vendor_template.replace("#customer_email", customer_cart.email)
        vendor_template = vendor_template.replace(
            "#shipping_address", f"{customer_cart.address}, {customer_cart.city}"
        )
        vendor_template = vendor_template.replace("#total_price", "₦ " + str(float(total_price)))
        vendor_template = vendor_template.replace("#product_details", product_details)
        vendor_template = vendor_template.replace(
            "#delivery_time", customer_cart.delivery_time.strftime("%b %d, %Y %I:%M %p")
        )

        # read the admin email and replace the tags
        with open("emails/order_placed_email_admin.html") as f:
            admin_template = f.read()

        admin_template = admin_template.replace("#business_name", business_name)
        admin_template = admin_template.replace("#customer_email", customer_cart.email)
        admin_template = admin_template.replace(
            "#shipping_address", f"{customer_cart.address}, {customer_cart.city}"
        )
        admin_template = admin_template.replace("#total_price", "₦ " + str(float(total_price)))
        admin_template = admin_template.replace("#product_details", product_details)
        admin_template = admin_template.replace(
            "#delivery_time", customer_cart.delivery_time.strftime("%b %d, %Y %I:%M %p")
        )

        # Create a multipart message and set headers
        customer_message = MIMEMultipart()
        customer_message["From"] = settings.EMAIL_HOST_USER
        customer_message["To"] = customer_cart.email
        customer_message["Subject"] = "Yay! Your order is confirmed!"

        # Add body to email
        customer_message.attach(MIMEText(customer_template, "html"))

        # convert to string
        customer_text = customer_message.as_string()

        # Create a multipart message and set headers
        vendor_message = MIMEMultipart()
        vendor_message["From"] = settings.EMAIL_HOST_USER
        vendor_message["To"] = vendor_email
        vendor_message["Subject"] = "A new order has been placed!"

        # Add body to email
        vendor_message.attach(MIMEText(vendor_template, "html"))

        # convert to string
        vendor_text = vendor_message.as_string()

        # Create a multipart message and set headers
        admin_message = MIMEMultipart()
        admin_message["From"] = settings.EMAIL_HOST_USER
        admin_message["To"] = settings.EMAIL_HOST_USER
        admin_message["Subject"] = "A new order has been placed!"

        # Add body to email
        admin_message.attach(MIMEText(admin_template, "html"))

        # convert to string
        admin_text = admin_message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, customer_cart.email, customer_text)
            server.sendmail(settings.EMAIL_HOST_USER, vendor_email, vendor_text)
            server.sendmail(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_USER, admin_text)

    except Exception as error:
        print(f"Error sending invitation email: {error}")


@shared_task(bind=True)
def send_30_minutes_to_delivery_email(self, cart_id: str):

    try:

        customer_cart = CustomerCart.objects.filter(id=cart_id).first()

        with open("emails/delivery_in_30_minutes_customer.html") as f:
            customer_template = f.read()

        customer_template = customer_template.replace("#order_code", customer_cart.code)

        # Create a multipart message and set headers
        customer_message = MIMEMultipart()
        customer_message["From"] = settings.EMAIL_HOST_USER
        customer_message["To"] = customer_cart.email
        customer_message["Subject"] = "Your order will be out for delivery soon!"

        # Add body to email
        customer_message.attach(MIMEText(customer_template, "html"))

        # convert to string
        customer_text = customer_message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, customer_cart.email, customer_text)

        print("done sending email")

    except Exception as error:
        print(f"Error sending invitation email: {error}")


@shared_task(bind=True)
def send_delivery_in_progress_email(self, cart_id: str):

    try:

        customer_cart = CustomerCart.objects.filter(id=cart_id).first()

        with open("emails/order_out_for_delivery.html") as f:
            customer_template = f.read()

        customer_template = customer_template.replace("#order_code", customer_cart.code)

        # Create a multipart message and set headers
        customer_message = MIMEMultipart()
        customer_message["From"] = settings.EMAIL_HOST_USER
        customer_message["To"] = customer_cart.email
        customer_message["Subject"] = "Your order is out for delivery!"

        # Add body to email
        customer_message.attach(MIMEText(customer_template, "html"))

        # convert to string
        customer_text = customer_message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, customer_cart.email, customer_text)

    except Exception as error:
        print(f"Error sending invitation email: {error}")


@shared_task(bind=True)
def send_order_delivered_email(self, cart_id: str):

    try:

        customer_cart = CustomerCart.objects.filter(id=cart_id).first()

        with open("emails/order_delivered.html") as f:
            customer_template = f.read()

        customer_template = customer_template.replace("#order_code", customer_cart.code)

        # Create a multipart message and set headers
        customer_message = MIMEMultipart()
        customer_message["From"] = settings.EMAIL_HOST_USER
        customer_message["To"] = customer_cart.email
        customer_message["Subject"] = "Order Delivered!"

        # Add body to email
        customer_message.attach(MIMEText(customer_template, "html"))

        # convert to string
        customer_text = customer_message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, customer_cart.email, customer_text)

    except Exception as error:
        print(f"Error sending invitation email: {error}")
