from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListAPIView
from rest_framework import viewsets, status
from rest_framework.response import Response 
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination 
from .models import MenuCategory, MenuItem
from .serializers import MenuCategorySerializer, MenuItemSerializer

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

class MenuItemSearchViewSet(viewsets.ViewSet):
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

class MenuItemIngredientsView(RetrieveAPIView):
    """
    Return all ingredients for the given MenuItem ID.
    """

    def get(self, request, pk):
        try:
            menu_item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)


        ingredients = menu_item.ingredients.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)

class MenuItemSearchViewSet(viewsets.ViewSet):

    # PUT  /Menu-items/<id>
    def update(self, request, pk=None):
        try:
            menu_item = MenuItem.objects.get(pk=pk)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found"},status=status.HTTP_404_NOT_FOUND
            )

        serializer = MenuItemSerializer(menu_item, data=request.data)

        if serializer.is_valid();
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
              
class MenuItemByCategoryView(ListAPIView):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        category_name = self.request.query_params.get('category', None)

        if category_name:
            return MenuItem.objects.filter(category__name__iexact=category_name)

        return MenuItem.objects.all()

class Table(models.Model):
    table_number = models.IntegerField()
    capacity = models.IntegerField()
    is_available = models.BooleanField(default=True) 

    def __str__(self):
        return f"Table {self.table_number}"           