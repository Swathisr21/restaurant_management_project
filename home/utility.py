from datetime import datetime, time
from .models import DailyOperatingHours
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import logging 
from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException


logger = logging.getLogger(__name__)


def send_order_confirmation_email(order_id, customer_email, customer_name, total_price):
    """
    Sends an order confirmation email to the customer.
    Returns a success or error message.
    """

    subject = f"Order Confirmation - Order #{order_id}"

    message = f"""
Hello {customer_name},

Thank you for your order!

Here are your order details:

Order ID: {order_id}
Total Price: {total_prince}

Your order is now being processed.
We will notify you once it is ready.

Thank you for choosing our restaurant!

Best regards,
Restaurant Team

"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email],
            fail_silently=False,
        )

        return {
            "success": True,
            "message": "Order confirmationemail sent successfully."
        }

    except SMTPException as e:
        logger.error(f"SMPT error while sending order email: {str(e)}")

        return {
            "success": False,
            "message": "An unexpectederror occured while sending the email."
        }    

def get_today_operating_hours():
    """
    Return today's operating hours as a tuple (open_time, close_time).
    if no record is found for today, returns (None, None).
    """
    # get the current day name 
    today_name = datetime.now().strftime('%A')
    
    try:
        # look up today's operating hours in the database
        hours = DailyOperatingHours.objects.get(day_of_week=today_name)
        return (hours.open_time, hours.close_time)
    except DailyOperatingHours.DoesNotExist:
       # if no record found, restaurant might be closed
    return None, None  

def is_restaurant_open():
    # Get current day and time
    now = datetime.now()
    current_day = now.weekday()
    current_time = now.time()

    # Weekdays (mon-fri):9 AM - 10 PM
    weekday_open = time(9, 0)
    weekday_close = time(22, 0)

    # Weekend (sat-sun):10 AM - 11 PM
    weekend_open = time(10, 0)
    weekend_close = time(23, 0)

    # Check if restaurant is open
    if current_day < 5:   # Monday-Friday
        return weekday_open <= current_time <= weekday_close
    else:   # Saturday-Sunday
        return weekend_open <= current_time <= weekend_close

def is_valid_email(email: str) -> bool:
    """
    Validates an email address.
    """ 
    validator = EmailValidator()

    try:
        validator(email)
        return True
    except ValidationError:
        return False        