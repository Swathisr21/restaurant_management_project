from django.contrib import admin

# Register your models here.
from .models import OrderStatus, Order


admin.site.register(OrderStatus)

# customer admin action:
    def mark_orders_processed(modeladmin, request, queryset):
    queryset.update(status="Processed")
# Optional Success Message:
    modeladmin.message_user(request, f"{queryset.count()} orders were marked as Processed.")

    @admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "ststus", "created_at")

    actions = [mark_orders_processed]