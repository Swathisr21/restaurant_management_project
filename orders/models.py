from django.db import models

# Create your models here.
from django.utils import timezone

# menu category  model
class MenuCategory(models.model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name

# order status
class OrderStatus(models.Model):
    name = mpdels.CharField(max_length=50, unique=True)


def __str__(self):
    return self.name

# coupon
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()


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