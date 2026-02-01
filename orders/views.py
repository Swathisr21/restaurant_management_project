from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from .serializers import OrderStatusUpdateSerializer

class OrderHistoryView(ListAPIView):
    """
    Returns the order history of the logged-in user.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-Created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class PaymentMethodListView(ListAPIView):
    """
    Returns all active payment methods.
    """
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentMethod.objects.filter(is_active=True) 
    
               