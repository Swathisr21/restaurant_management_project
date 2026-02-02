from django.shortcuts import render

# Create your views here.

from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import viewsets, status
from rest_framework.response import Response 
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination 
from .models import MenuCategory, MenuItem, Table, UserReview
from .serializers import MenuCategorySerializer, MenuItemSerializer, TableSerializer, UserReviewSerializer
from .utils.validation_utils import is_valid_email
from rest_framework.permissions import IsAuthenticated 

if not is_valid_email(user_email):
    return Response({"error": "Invalid email"}, status=400)

class CreateUserReviewView(CreateAPIView):
    """
    Create a new review for a menu item.
    """
    serializer_class = UserReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MenuItemReviewListView(ListAPIView):
    """
    Retrieve all reviews for a specific menu item.
    """
    serializer_class = UserReviewSerializer
    
    def get_queryset(self):
        menu_item_id = self.kwargs.get("menu_item_id")
        return UserReview.objects.filter(
            menu_item_id=menu_item_id
        ).order_by("-created_at")            
    

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

class TableDetailView(RetrieveAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class AvailableTablesAPIView(ListAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.filter(is_available=True)

class DailySpecialsView(APIView):
    """
    Returns all menu items marked as daily specials.
    """

    def get(self, request):
        specials = MenuItem.objects.filter(is_daily_special=True)

        serializer = DailySpecialSerialzer(specials, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class MenuCategoryViewSet(ModelViewSet):
    """
    Handles CRUD operations for menu Categories:
    - List
    - Retrieve
    - Create
    - Update
    - Delete
    """
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer                   