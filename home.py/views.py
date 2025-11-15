from django.shortcuts import render

# DRF imports
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# Models & Serializers
from .models import MenuCategory, MenuItem
from .serializers import MenuCategorySerializer, MenuItemSerializer


# -------------------------
# 1. CATEGORY LIST VIEW
# -------------------------

class MenuCategoryListView(ListAPIView):
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer


# -------------------------
# 2. FEATURED MENU ITEMS
# -------------------------

class FeaturedMenuItemView(ListAPIView):
    """
    API endpoint to list only featured menu items.
    """
    queryset = MenuItem.objects.filter(is_featured=True)   # FIXED: objects, removed :
    serializer_class = MenuItemSerializer


# -------------------------
# 3. PAGINATION CLASS
# -------------------------

class MenuItemPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# -------------------------
# 4. SEARCH VIEWSET
# -------------------------

class MenuItemSearchViewset(viewsets.ViewSet):   # FIXED: ViewSet (not Viewsets)
    pagination_class = MenuItemPagination

    def list(self, request):
        search_query = request.GET.get('q', '')

        # Search by name
        queryset = MenuItem.objects.filter(name__icontains=search_query)

        # Paginate
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = MenuItemSerializer(paginated_queryset, many=True)

        return paginator.get_paginated_response(serializer.data)
