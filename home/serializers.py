from rest_framework import serializers
from .models import MenuCategory, MenuItem, Table, UserReview

class UserReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = UserReview
        fields = [
            "id",
            "user",
            "menu_item",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["id", "user", "created_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.validationError(
                "Rating must be between 1 and 5."
            )
        return value        

class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'description']

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

class DailySpecialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = [
            "id",
            "name",
            "price",
            "is_daily_special"
        ]
