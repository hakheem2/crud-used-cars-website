from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime

def send_order_confirmation(order):
    subject = f"Order Confirmation - {order.order_id}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = [order.email, settings.DEFAULT_FROM_EMAIL]  # customer + yourself

    html_content = render_to_string(
        'orders/order_template.html',
        {
            'order': order,
            'website_url': 'https://carsmaxautos.com',
            'year': datetime.now().year,
        }
    )

    text_content = f"""
        Hi {order.name},

        Thank you for your purchase!
        Your order ORD-{order.order_id} has been successfully placed.

        Customer Information:
        Name: {order.name}
        Email: {order.email}
        Phone: {order.phone}
        Address: {order.address}

        Order Details:
        Car Name: {order.car_name}
        Model: {order.car_model}
        Year: {order.car_year}
        Price: ${order.car_price}

        Visit our website: https://carsmaxautos.com
        """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
