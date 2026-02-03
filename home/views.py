from rest_framework.views import APIView
from rest_framework.response import response
from rest_framework import status
from .models import Restaurant
from .serializers import RestaurantSerializer

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