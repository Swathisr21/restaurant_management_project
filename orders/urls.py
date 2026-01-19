from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    cancel_order,
    complete_order,
    edit_order,
    delete_order,
    invoice_page
)

router = DefaultRouter()
router.register('order', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),

    path("order/<int:order_id>/cancel/", cancel_order, name="cancel_order"),
    path("order/<int:order_id>/complete/", complete_order, name="complete_order"),
    path("order/<int:order_id>/edit/", edit_order, name="edit_order"),
    path("order/<int:order_id>/delete/", delete_order, name="delete_order"),
    path("order/<int:order_id>/invoice/", invoice_page, name="invoice_page"),
]
