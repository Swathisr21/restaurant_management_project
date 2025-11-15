from django.db import models
from django.contrib.auth.models import user

# Create your models here.
from django.utils import timezone
from .utility import generate_coupon_code

# menu category  model
class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name

# order status
class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)


def __str__(self):
    return self.name

# coupon
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()

    def save(self, *args, **kwargs):
        # if no code entered ,generate one automatically 
        if not self.code:
           self.code = generate_coupon_code()
        super().save(*args, **kwargs)   

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% off)"

# order 
class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    Created_at = models.DateTimeField(auto_now_add=True)

    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status.name if self.status else 'No Status'}"        

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    has_delivery = models.BooleanField(default=False)

    def __str__(self):
        return self.name