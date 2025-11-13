from django.db import models

# Create your models here.
class MenuCategory(model.Model):
    name = models.CharField(max_length=100)

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name