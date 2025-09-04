from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime
import resend  # Make sure resend is installed

def send_order_confirmation(order):
    """
    Sends order confirmation email to the customer and sends a separate copy to yourself.
    """

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
    Your order ORD-{order.order_id} for {order.car_name} has been successfully placed.
    
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

    client = resend.Emails()

    try:
        # Send to customer
        client.send({  # type: ignore
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [order.email],
            "subject": "Order Confirmation",
            "html": html_content,
            "text": text_content,
        })
        print("✅ Email sent:")
    except Exception as e:
        print("❌ Resend error:", e)


    try:
        # Send a separate copy to yourself
        client.send({  # type: ignore
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [settings.DEFAULT_FROM_EMAIL],
            "subject": "Order Confirmation",
            "html": html_content,
            "text": text_content,
        })
        print("✅ Email sent:")
    except Exception as e:
        print("❌ Resend error:", e)




    # client = resend.Emails(api_key=settings.RESEND_API_KEY)
    # # Send with Resend
    # try:
    #     response = resend.Emails.send({
    #         "from": settings.DEFAULT_FROM_EMAIL,
    #         "to": [order.email, settings.DEFAULT_FROM_EMAIL],
    #         "subject": f"Order Confirmation",
    #         "html": html_content,
    #         "text": text_content,
    #     })
    #     print("✅ Email sent:", response)
    # except Exception as e:
    #     print("❌ Resend error:", e)
