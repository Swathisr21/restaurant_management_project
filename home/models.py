from django.db import models
from django.db.models import Count
from datetime import datetime, timedelta 
from django.contrib.auth.models import User
from .models import MenuItem

class UserReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(
        "MenuItem",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField()
    related_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.menu_item.name}"

# Menu Item Manager
class MenuItemManager(models.Manager):
    def get_top_selling_items(self, num_items=5):
        return (
            self.get_queryset()
            .annotate(order_count=Count("orderitem"))
            .order_by("-order_count")[:num_items]
        )

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        "MenuCategory",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # New Field 
    is_daily_special = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Menu Category
class MenuCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

# Daily Special Manager        
class DailySpecialManager(models.Manager):
    def upcoming(self):
        today = datetime.date.today()
        return super().get_queryset().filter(date__gte=today, available=True)
        
# Daily Special
class DailySpecial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    date = models.DateField()

    objects = DailySpecialManager()


    @staticmethod
    def get_random_special():
        specials = DailySpecial.objects.filter(available=True)
        return specials.order_by("?").first() if specials.exists() else None

    def __str__(self):
        return self.name

# NutritionalInformation     
class NutritionalInformation(models.Model):
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="nutrition"
    )

    calories = models.IntegerField()
    protein_grams = models.DecimalField(max_digits=5, decimal_places=2)
    fat_grams = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrate_grams = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Nutritional Info for {self.menu_item.name}      

# Ingredients
class Ingredient(models.Model): 
    name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name


# Update MenuItem model by adding ingredients field 
class MenuItem(models.Model)
    name = models.CharField(max_length=100)
    description = models.TextField() 
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_featured = models.BooleanField(default=False)

    category = models.ForeignKey(
        'MenuCategory',
        on_delete=models.CASCADE,
        related_name='menu_item',
        null=True,
        blank=True
    )
    objects = MenuItemManager()

    # New field
    ingredients = models.ManyToManyField(Ingredient, related_name='menu_items', blank=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"          

# Restaurant
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    opening_hours = models.CharField(
        max_length=100,
        help_text="Example: Mon-Sun 9:00 AM - 10:00 PM"
    )
    has_delivery = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# LoyaltyProgram
class LoyaltyProgram(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True
    )

    points_Required = models.IntegerField(
        unique=True
    )  

    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    description = models.TextField()

    def __str__(self):
        return self.name

class Reservation(models.Model):
    """
    Stores reservations for a restaurant.
    """

    customer_name = models.CharField(max_length=100)
    reservation_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.customer_name} - {self.reservation_date} ({self.start_time} to {self.end_time})"       
    
    @classmethod
    def fine_available_slots(
        cls,
        reservation_date,
        range_start,
        range_end,
        slot_duration_minutes=60
    ):
        """
        Find available reservation slots within a given time range.
        """

        existing_reservations = cls.objects.filter(
            reservation_date=reservation_date
        )

        available_slots = []

        current_start = datetime.combine(reservation_date, range_start)
        boundary_end = datetime.combine(reservation_date, range_end)
        slot_delta = timedelta(minutes=slot_duration_minutes)

        while current_start + slot_delta <= boundary_end:
            current_end = current_start + slot_delta

            # Check for overlapping reservations 
            overlap = existing_reservations.filter(
                start_time__lt=current_end.time(),
                end_time__gt=current_start.time()
            ).exists()

            if not overlap:
                available_slots.append(
                    (current_start.time(), current_end.time())
                )

                current_start += slot_delta

        return available_slots        