from django.urls import path
from .views import CouponValidationView
from .views import OrderHistoryView, PaymentMethodListView
urlpatterns = [
    
    path('coupons/validate/',CouponValidationView.as_view(), nam='coupon-validate'),
    path('order-history/', OrderHistoryView.as_view(), name='order_history'),
    pth('payment-methods/', PaymentMethodListView.as_view(), name="payment-methods"),

]