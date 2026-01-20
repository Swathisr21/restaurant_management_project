import string
import secrets
from django.db.models import Sum
from decimal import Decimal
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from smtplib import SMTPException

logger = logging.getLogger(__name__)

# Email sender
def send_email(recipient_email, subject, message):
    try:
        validate_email(recipient_email)

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return True
    except ValidationError:
        logger.error(f"Invalid email: {recipient_email}")
        return False
    except Exception as e:
        logger.error(f"Email error :{str(e)}")
        return False

def generate_unique_order_id(length=8):
    """
    Generate a unique, short alphanumeric order ID.
    Example: X9K2A7PZ
    """
    from .models import Order
    characters = string.ascii_uppercase + string.digits

    while True:
        order_id = ''.join(secrets.choice(characters) for _ in range(length))
        if not Order.objects.filter(order_id=order_id).exists():
            return order_id
            
def send_order_confirmation_email(order_id, customer_email, customer_name, total_price):
    """
    Sends an order confirmation email to the customer.
    Returns a success or error message.
    """

    subject = f"Order Confirmation - Order #{order_id}"

    message = f"""

    Thank you for your order!

    Here are your order details:

    Order ID: {order_id}
    Total price: {total_price}

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
            "message": "Order confirmation email sent successfully."
        }

    except SMTPException as e:
        logger.error(f"SMTP error while sending order email: {str(e)}")

        return {
            "success": False,
            "message": "Failed to send email due to email server error."
        }

    except Exception as e:
        logger.error(f"Unexpected error while sending order email: {str(e)}")

        return {
            "success": False,
            "message": "An unexpected error occurred while sending the email."       
        }
                            

def generate_coupon_code(length=10):
    """ Generates a unique random alphanumeric coupon code."""
    from .models import Coupon
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))
        #  check if this code already exists in database
        if not Coupon.objects.filter(code=code).exists():
            return code

def get_daily_sales_total(date):
    """
    Return the total sales for a given date.
    :param date: A python date object.
    :return : Decimal total of sales for that day , or 0 if none.
    """
    from .models import Order
     # orders QuerySet
    orders = Order.objects.filter(created_at__date=date)
    result = orders.aggregate(total_sum=Sum('total_price'))
    total = result.get('total_sum')

    if total is None:
        return Decimal("0.00")
    return total

def calculate_tip_amount(order_total, tip_percentage):
    """
    calculate the tip amount for a given order total and tip percentage.
    
    """
    
    # convert values to decimal for accurate money calculation
    order_total = Decimal(order_total)
    tip_percentage = Decimal(tip_percentage)

    tip_amount = order_total * (tip_percentage / Decimal(100))

    # round to 2 decimal places
    return round(tip_amount, 2)


def validate_phone_number(phone_number):
    """
    Validate phone number format.
    Basic validation - should be 10 digits.
    """
    import re
    pattern = r'^\d{10}$'
    return bool(re.match(pattern, phone_number))


def get_restaurant_open_status():
    """
    Check if restaurant is currently open based on opening days.
    For now, simple implementation - restaurant is open Mon-Sun.
    """
    from datetime import datetime
    current_day = datetime.now().strftime('%a')
    # This is a basic implementation - in real world, you'd have opening hours
    open_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    return current_day in open_days


def get_todays_restaurant_hours():
    """
    Return today's restaurant hours.
    Basic implementation.
    """
    return "9:00 AM - 10:00 PM"


def get_random_daily_special():
    """
    Get a random daily special from featured menu items.
    """
    from home.models import MenuItem
    featured_items = MenuItem.objects.filter(is_featured=True)
    if featured_items.exists():
        import random
        return random.choice(list(featured_items))
    return None


def validate_email_address(email):
    """
    Validate email address format.
    """
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def top_selling_menu_items(limit=5):
    """
    Custom manager method to get top-selling menu items.
    """
    from django.db.models import Count
    from .models import OrderItem

    return OrderItem.objects.values('menu_item__name') \
        .annotate(order_count=Count('menu_item')) \
        .order_by('-order_count')[:limit]


def upcoming_daily_specials():
    """
    Custom manager to filter upcoming daily specials.
    For now, just return featured items.
    """
    from home.models import MenuItem
    return MenuItem.objects.filter(is_featured=True)
