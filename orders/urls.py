from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    CouponViewSet,
    PaymentMethodViewSet,
    LoyaltyProgramViewSet,
    NutritionalInfoViewSet,
    IngredientListView,
    ContactViewSet,
    cancel_order,
    complete_order,
    edit_order,
    delete_order,
    invoice_page,
    kitchen_orders,
    update_order_status,
    submit_review,
    customer_reviews,
    inventory_management,
    update_inventory
)

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')
router.register('coupon', CouponViewSet, basename='coupon')
router.register('payment-method', PaymentMethodViewSet, basename='payment-method')
router.register('loyalty-program', LoyaltyProgramViewSet, basename='loyalty-program')
router.register('nutritional-info', NutritionalInfoViewSet, basename='nutritional-info')
router.register('contact', ContactViewSet, basename='contact')

urlpatterns = [
    path('', include(router.urls)),

    # Ingredients API
    path("ingredients/", IngredientListView.as_view(), name="ingredients"),

    # Order management URLs
    path("order/<int:order_id>/cancel/", cancel_order, name="cancel_order"),
    path("order/<int:order_id>/complete/", complete_order, name="complete_order"),
    path("order/<int:order_id>/edit/", edit_order, name="edit_order"),
    path("order/<int:order_id>/delete/", delete_order, name="delete_order"),
    path("order/<int:order_id>/invoice/", invoice_page, name="invoice_page"),

    # Kitchen and staff features
    path("kitchen/", kitchen_orders, name="kitchen_orders"),
    path("order/<int:order_id>/status/<str:new_status>/", update_order_status, name="update_order_status"),

    # Customer reviews
    path("order/<int:order_id>/review/", submit_review, name="submit_review"),
    path("reviews/", customer_reviews, name="customer_reviews"),

    # Inventory management
    path("inventory/", inventory_management, name="inventory_management"),
    path("inventory/<int:item_id>/update/", update_inventory, name="update_inventory"),
]
