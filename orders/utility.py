import string
import secrets
from .models import Coupon
from django.db.models import sum
from .models import Order

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

    orders = Order.objects.filter(created_at_date=date)
    result = order.aggregate(total_sum=Sum('total_price'))['tital_sum']
    return result if result is not None else 0            