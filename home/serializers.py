from rest_framework import serializers
from .models import MenuCategory
from .models import MenuItem

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id','name']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta = MenuItem
    fields = '__all__'        