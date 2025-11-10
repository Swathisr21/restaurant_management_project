from django.urls import path
from .views import CouponValidationView

urlpatterns = [
    
    path('coupons/validate/',CouponValidationView.as_view(), nam='coupon-validate'),


]