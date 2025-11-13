from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListAPIView
from .models import MenuCategory
from .serializers import MenuCategorySerializer
from .models import MenuItem
from .serializers import MenuItemSerializer

class MenuCategoryListView(ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class FeaturedMenuItemView(ListAPIView):
    """
    API endpoin to list only the menu items 
    """
    queryset = MenuItem.Objects.filter(is_featured=True):
    serializer_class = MenuItemSerializer   
