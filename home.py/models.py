from django.db import models

# Create your models here.
class MenuCategory(models.Model):
    name = models.CharField(max_length=100)

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class DailySpecial(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

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
    