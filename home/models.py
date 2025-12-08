from django.db import models
import datetime, MenuItem
from django.db.models import Count

class MenuItemManager(models.Manager):
    def get_top_selling_items(self, num_items=5):
        return (
            self.get_queryset()
            .annotate(order_count=Count("orderitem"))
            .order_by("-order_count")[:num_items]
        )

class MenuCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"
class DailySpecialManager(models.Manager):
    def upcoming(self):
        today = datetime.date.today()
        return super().get_queryset().filter(date__gte=today, available=True)
        
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
        if not specials.exists():
            return None

        return specials.order_by("?").first()

    def __str__(self):
        return self.name    
class NutritionalInformation(models.Model):
    menu_item = models.ForeignKey(
        'MenuItem',
        on_delete=models.CASCADE,
        related_name='nutrition'
    )

    calories = models.IntegerField()
    protein_grams = models.DecimalField(max_digits=5, decimal_places=2)
    fat_grams = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrate_grams = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Nutritional Info for {self.menu_item.name} - {self.calories} calories"                     

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

    def __str__(self):
        return self.name

    # New field
    ingredients = models.ManyToManyField(Ingredient, related_name='menu_items', blank=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"          

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    has_delivery = models.BooleanField(default=False)

    # New Field: operating days
    operating_days = models.CharField()
       max_length=100,
       help_text="comma-separated days (e.g., Mon,Tue,Wed,Thu,Fri)"
    )

    def __str__(self):
        return self.name
