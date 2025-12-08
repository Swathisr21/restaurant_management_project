from django.contrib import admin
from .models import Restaurant
from .models import LoyaltyProgram


# Register your models here.

class RestaurantAdmin(admin.ModelAdmin):

# 3. Show these fields in List view
List-display = ('name', 'address', 'phone_number', 'email', 'is_active')

# 4. Enable search by name or address
search_fields = ('name', 'address')

# 5. Filter by active/inactive if the has an is_active field
list_filter = ('is_active',)

# 6. Register Restaurant model with the admin
admin.site.register(Restaurant, RestaurantAdmin)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'has_delivery', 'operating_days')

admin.site.register(LoyaltyProgram)  