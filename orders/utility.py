import string
import secrets
from decimal import Decimal
from django.db.models import Sum


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
def generate_coupon_code():
    from .models import Coupon   # lazy import → breaks circular import
    # your logic...

