from rest_framework.views import APIView
from rest_framework.response import response
from rest_framework import status
from .models import Restaurant, MenuItem
from .serializers import RestaurantSerializer, MenuItemAvailabilitySerializer

class UpdateMenuItemAvailabilityView(APIView):
    """
    Update menu item availability
    """

    def put(self, request, menu_item_id):
        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return Response(
                {"error": "Menu item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MenuItemAvailabilitySerializer(data=request.data)

        if serializer.is_valid():
            menu_item.is_available = serializer.validated_data["is_available"]
            menu_item.save()

            return Response(
                {
                    "message": "Menu item availability updated successfully",
                    "menu_item_id": menu_item.id,
                    "is_available": menu_item.is_available,
                },
                status=status.HTTP_200_OK
            )        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class RestaurantInfoView(APIView):
    """
    GET restaurant details
    """

    def get(self, request):
        restaurant = Restaurant.objects.first()

        if not restaurant:
            return Response(
                {"error": "Restaurant information not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)    