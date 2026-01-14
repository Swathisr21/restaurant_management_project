from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User

from .utility import generate_coupon_code, generate_unique_order_id


#  Custom Manager
class ActiveOrderManager(models.Manager):
    def get_active_orders(self):
        return self.filter(status__name__in=["pending", "processing"])


#  Menu Category Model
class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


#  Order Status Model
class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


#  Coupon Model
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_until = models.DateField()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_coupon_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} ({self.discount_percentage}% off)"


#  Menu Item Model  (ONLY IF you don't have it in home app)
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


#  Order Model
class Order(models.Model):
    order_id = models.CharField(max_length=12, unique=True, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    customer_name = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True)

    objects = ActiveOrderManager()

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_unique_order_id()
        super().save(*args, **kwargs)

    def get_unique_item_names(self):
        """
        Returns unique menu item names in this order.
        """
        items = self.orderitem_set.select_related("menu_item")
        return list({item.menu_item.name for item in items})

    def calculate_total(self):
        """
        Total = sum(price * quantity) for all order items.
        """
        total = Decimal("0.00")

        for item in self.orderitem_set.all():
            total += item.price * item.quantity

        return total

    def __str__(self):
        return f"Order {self.order_id}"


#  Order Item Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    # store item price at the time of order
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"


#  Restaurant Model
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    has_delivery = models.BooleanField(default=False)

    def __str__(self):
        return self.name


#  Payment Method Model
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
