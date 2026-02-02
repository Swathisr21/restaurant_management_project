from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order
from rest_framework.decorators import permission_classes
from .serializers import OrderSerializer
from .serializers import OrderStatusUpdateSerializer, OrderCancelSerializer

class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderStatusUpdateSerializer(data=request.data)

        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            new_status = serializer.validated_data['status']

            try:
                order = Order.objects.get(id=order_id)
                
                # Optional : restrict update to order owner
                if order.user != request.user:
                    return Response(
                        {"error": "You are not allowed to update this order."},
                        status=status.HTTP_403_FORBIDDEN 
                    )

                order.status = new_status
                order.save()

                return Response(
                    {
                        "message": "Order status updated successfully.",
                        "order_id": order.id,
                        "new_status": order.status
                    },
                    status=status.HTTP_200_OK
                )

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                     
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_status(request, order_id):
    """
    Retrieve the current status of an order by order ID.
    """

    try:
        order = Order.objects.get(order_id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(
        {
            "order_id": order.order_id,
            "status": order.status.name if order.status else None
        },
        status=status.HTTP_200_OK
    )        
        
