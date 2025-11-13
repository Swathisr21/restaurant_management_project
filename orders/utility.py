import string
import secrets
from .models import Coupon

def generate_coupon_code(length=10):
    """ Generates a unique rando alphanumeric coupon code."""
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))
        #  check if this code already excits in database
        if not Coupon.objects.filter(code=code).exists():
            return code