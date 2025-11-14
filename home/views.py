from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination 
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

class MenuItemPagination(PageNumberPagination):
    page_size = 10 
    page_size_query_param = 'page_size'
    max_page_size = 100

class MenuItemSearchViewset(viewsets.Viewsets):
    pagination_class = MenuItemPagination

    def list(self, request):
        search_query = request.GET.get('q', '')

        #search by name
        queryset = MenuItem.objects.filter(name__icontains=search_query)

        #paginate results
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = MenuItemSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)