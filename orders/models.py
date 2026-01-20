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


#  Order Model
class Order(models.Model):
    order_id = models.CharField(max_length=12, unique=True, editable=False, default='')

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
    menu_item = models.ForeignKey('home.MenuItem', on_delete=models.CASCADE)  # Reference to home.MenuItem

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
    opening_days = models.CharField(max_length=100, default='Mon-Sun')  # For restaurant opening days

    def __str__(self):
        return self.name


#  Payment Method Model
class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


#  Loyalty Program Model
class LoyaltyProgram(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    tier = models.CharField(max_length=20, default='Bronze')

    def __str__(self):
        return f"{self.user.username} - {self.points} points"


#  Nutritional Information Model
class NutritionalInfo(models.Model):
    menu_item = models.OneToOneField('home.MenuItem', on_delete=models.CASCADE)
    calories = models.IntegerField()
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)
    fat = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Nutrition for {self.menu_item.name}"


#  Ingredients Model
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    menu_item = models.ForeignKey('home.MenuItem', on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return self.name


#  Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"


#  Customer Review Model
class CustomerReview(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)  # For moderation

    def __str__(self):
        return f"Review for Order {self.order.order_id} - {self.rating} stars"


#  Staff/Employee Model
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=50, choices=[
        ('manager', 'Manager'),
        ('chef', 'Chef'),
        ('waiter', 'Waiter'),
        ('cashier', 'Cashier'),
        ('cleaner', 'Cleaner'),
    ])
    phone = models.CharField(max_length=15, blank=True)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"


#  Inventory/Stock Model
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=[
        ('ingredients', 'Ingredients'),
        ('beverages', 'Beverages'),
        ('supplies', 'Supplies'),
        ('equipment', 'Equipment'),
    ])
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, choices=[
        ('kg', 'Kilograms'),
        ('g', 'Grams'),
        ('l', 'Liters'),
        ('ml', 'Milliliters'),
        ('pieces', 'Pieces'),
        ('boxes', 'Boxes'),
    ])
    minimum_threshold = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=100, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.quantity <= self.minimum_threshold

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"


#  Shift Management Model
class Shift(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    role = models.CharField(max_length=50)  # Can override staff role for this shift

    class Meta:
        unique_together = ['staff', 'date', 'start_time']

    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.date}"
