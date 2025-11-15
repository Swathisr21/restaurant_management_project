from rest_framework import serializers
from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'is_active', 'valid_from', 'valid_untill']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'created_at', 'total_price', 'customer_name']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        field = ['item_name', 'quantity','price']