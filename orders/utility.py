import string
import secrets
from .models import Coupon
from django.db.models import sum
from .models import Order
from decimal import Decimal
import logging
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from smtplib import SMTPException
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

def update_order_status(order_id, new_status):
    """
    Update the status of an order.

    Args:
        order_id (int): ID of the order to update
        new_status (str): New status to set (e.g., 'PENDING', 'PROCESSING', 'DELIVERED')

    Returns:
        tuple (bool, str):
            - True, success message if updated
            - False, error message if failed
    """
    try:
        order = Order.objects.get(id=order_id)

        old_status = order.status
        order.status = new_status
        order.save()

        logger.info(
            f"Order {order_id} status changed from {old_status} to {new_status}"
        )

        return True, "Order status updated successfully."

    except ObjectDoesNotExist:
        logger.error(f"Order with ID {order_id} not found.")
        return False, "Order not found."

    except Exception as exc:
        logger.exception(
            f"Unexpected error while updating order {order_id}: {exc}"
        )
        return False, "Failed to update order status."                    

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
    characters = string.ascii_uppercase + string.digits

    while True:
        order_id = ''.join(secrets.choice(characters) for _ in range(length))
        if not Order.objects.filter(order_id=order_id).exsits():
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

    Best resards,
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
               "message": "Order confirmation email sent succeesfully."
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
    """ Generates a unique rando alphanumeric coupon code."""
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))
        #  check if this code already excits in database
        if not Coupon.objects.filter(code=code).exists():
            return code

def get_daily_sales_total(date):
    """
    Return the total sales for a given date.
    :param date: A python date object.
    :return : Decimal total of sales for that day , or 0 if none.
    """
     # orders QuerySet
    orders = Order.objects.filter(created_at_date=date)
    result = orders.aggregate(total_sum=Sum('total_price'))
    total = result.get('total_sum')

    if total is None:
        return 0
    return total

def calculate_tip_amount(order_total, tip_percentage):
    """
    calculate the tip amount for a given ordder total and tip percentage.
    
    """
    
    # convert values to decimal for accurate money calculation
    order_total = Decimal(order_total)
    tip_percentage = Decimal(tip_percentage)

    tip_amount = order_total * (tip_percentage / Decimal(100))

    # round to 2 decimal places
    return round(tip_amount, 2)

def calculate_order_total(order_items):
    """
    Calculate the total price of an order.

    Each item in order_items is expected to have:
    - price (Decimal or numeric)
    - quantity (int)

    Args:
        order_items (iterable): List or queryset of order items

    Returns:
        Decimal: Total order cost
    """

    total = Decimal("0.00")

    # Handel empty list or None safely
    if not order_items:
        return total

    for item in order_items:
        # Ensure price and quantity exist
        price = Decimal(item.price)
        quantity = int(item.quantity)

        total += price * quantity

    return total             