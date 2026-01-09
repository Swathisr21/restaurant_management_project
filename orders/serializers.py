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
    item_name = serializers.CharField(source='menu_item.name', read_only=True)
    price = serializers.DecimalField(
        source='Menu_item.price',
        max_digits=8,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['item_name', 'quantity','price']                

class OrderSerializer(serializers.ModelSerializer):
    status = OrderStatusSerializer(read_only=True)
    items = OrderItemSerializer(
        source='orderitem_set',
        many=True,
        read_only=True
    )

    class Meta:
        model Order
        fields = [
            'id',
            'order_id',
            'customer_name',
            'Created_at',
            'status',
            'items',
        ]        