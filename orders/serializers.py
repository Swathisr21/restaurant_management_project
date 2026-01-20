from rest_framework import serializers
from .models import Order, OrderItem, Coupon, PaymentMethod, LoyaltyProgram, NutritionalInfo, Ingredient, Contact
from home.models import MenuItem
from home.serializers import MenuItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_detail = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','menu_item','menu_item_detail','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'customer_name', 'created_at', 'status', 'status_name', 'total_amount', 'items']
        read_only_fields = ['order_id']

    def get_total_amount(self, obj):
        return obj.calculate_total()

    def create(self, validated_data):
        # Note: items are handled separately through a custom endpoint
        # For now, just create the order without items
        return Order.objects.create(**validated_data)


# Coupon Serializer
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


# Payment Method Serializer
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


# Loyalty Program Serializer
class LoyaltyProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyProgram
        fields = '__all__'


# Nutritional Info Serializer
class NutritionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionalInfo
        fields = '__all__'


# Ingredient Serializer
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


# Contact Serializer
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        read_only_fields = ['created_at', 'is_resolved']
