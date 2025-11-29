from rest_framework import serializers
from .models import Coupon, Order, OrderStatus, OrderItem


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'is_active', 'valid_from', 'valid_until']

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ['id', 'name']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item_name', 'quantity','price']                

class OrderSerializer(serializers.ModelSerializer):
    status = OrderStatusSerializer(read_only=True)

    class Meta:
        model Order
        fields = [
            'id',
            'customer_name',
            'Created_at',
            'status',
        ]        