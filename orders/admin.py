from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
from .models import OrderStatus, Order, PaymentMethod


admin.site.register(OrderStatus)
admin.site.register(PaymentMethod)

def mark_orders_processed(modeladmin, request, queryset):
    queryset.update(status="Processed")
    # Optional Success Message:
    modeladmin.message_user(request, f"{queryset.count()} orders were marked as Processed.")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "status", "created_at")

    actions = [mark_orders_processed]
