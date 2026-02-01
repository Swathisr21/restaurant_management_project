from rest_framework import serializers
from .models import Coupon, Order, OrderStatus, OrderItem


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_percentage', 'is_active', 'valid_from', 'valid_until']

class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Serializer to update order status
    """
    order_id = serializers.CharField()
    status = serializers.CharField()
    class Meta:
        model = OrderStatus
        fields = ['id', 'name']

    def validate_status(self, value):
        allowed_statuses = ["pending", "processing", "completed"]    
        
        if value.lower() not in allowed_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Allowed values: {allowed_statuses}"
            )
        return value.lower()

    def validate_order_id(self, value):
        if not Order.objects.filter(order_id=value).exists():
            raise serializers.ValidationError("Order with this ID does not exist.")
        return value

                   
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
    created_at = serializers.DateTimeField(
        source='Created_at',
        read_only=True
    )
    class Meta:
        model = Order
        fields = [
            'id',
            'customer_name',
            'created_at',
            'status',
            'items',
        ]        