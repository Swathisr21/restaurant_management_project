from django.urls import path
from .views import CouponValidationView, OrderStatusUpdateView, get_order_status
from .views import OrderHistoryView, PaymentMethodListView, CancelOrderView, UpdateOrderStatusView
urlpatterns = [
    
    path('coupons/validate/',CouponValidationView.as_view(), nam='coupon-validate'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
    path('payment-methods/', PaymentMethodListView.as_view(), name="payment-methods"),
    path('orders/update-status/', OrderStatusUpdateView.as_view(), name='order-update-status'),
    path('orders/cancel/', CancelOrderView.as_view(), name="cancel-order"),
    path('orders/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('order/status/<str:order_id>/', get_order_status, name='order-status'),
]
