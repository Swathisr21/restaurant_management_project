from django.contrib import admin

# Register your models here.
from .models import OrderStatus


admin.site.register(OrderStatus)