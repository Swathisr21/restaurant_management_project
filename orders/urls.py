from django.urls import path
from .views import CouponValidationView, OrderStatusUpdateView
from .views import OrderHistoryView, PaymentMethodListView, CancelOrderView
urlpatterns = [
    
    path('coupons/validate/',CouponValidationView.as_view(), nam='coupon-validate'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
    path('payment-methods/', PaymentMethodListView.as_view(), name="payment-methods"),
    path('orders/update-status/', OrderStatusUpdateView.as_view(), name='order-update-status'),
    path('orders/cancel/', CancelOrderView.as_view(), name="cancel-order"),
]
