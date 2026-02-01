from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from .serializers import OrderStatusUpdateSerializer, OrderCancelSerializer

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

class CancelOrderView(APIView):
    """
    Allows a user to cancel their own order
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = OrderCancelSerializer(
            data=request.data,
            context={"request": request}
        )        
    
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST 
            )

        order_id = serializer.validated_data["order_id"]
        order = Order.objects.get(order_id=order_id)

        # Set status to Cancelled
        cancelled_status = OrderStatus.objects.get(name__iexact="cancelled")
        order.status = cancelled_status
        order.save()

        return Response(
            {
                "message": "Order cancelled successfully.",
                "order_id": order.order_id,
                "status": "Cancelled"
            },
            status=status.HTTP_200_OK
        )

        
