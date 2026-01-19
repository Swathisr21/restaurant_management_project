from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('menu/', views.menu_page, name='menu'),
    path('order/', views.order_page, name='order'),
    path('my-orders/', views.my_orders, name='my_orders'),

    # IMPORTANT
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('order/<int:order_id>/invoice/', views.invoice_page, name='invoice_page'),
]
