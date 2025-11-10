from django.db import models

# Create your models here.
from django.utils import timezone


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()


    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% off)"