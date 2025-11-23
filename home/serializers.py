from rest_framework import serializers
from .models import MenuCategory, MenuItem, Table

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id','name']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
    fields = '__all__' 

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
    
    # Custom validation
    def validate_price(self, value):
        if value <= 0:
            raise serializers.validationError("Price must be a positive number")
        return value  

class TableSerializer(serializers.ModelSerializers):
     class Meta:
        model = Table
        fields = '__all__'

