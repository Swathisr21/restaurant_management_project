from rest_framework import serializers
from .models import Order, OrderItem
from products.models import MenuItem
from products.serializers import MenuItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_detail = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id','menu_item','menu_item_detail','quantity','price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id','customer_name','table_number','total_amount','is_completed','created_at','items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        total = 0
        for item in items_data:
            menu = MenuItem.objects.get(pk=item['menu_item'].id) if hasattr(item['menu_item'],'id') else MenuItem.objects.get(pk=item['menu_item'])
            price = menu.item_price * item.get('quantity',1)
            OrderItem.objects.create(order=order, menu_item=menu, quantity=item.get('quantity',1), price=price)
            total += price
        order.total_amount = total
        order.save()
        return order
