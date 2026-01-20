from django.urls import path
from .views import (
    MenuCategoryListView,
    FeaturedMenuItemView,
    MenuItemSearchViewSet,
    MenuItemViewSet,
    TableDetailView,
    AvailableTablesAPIView,
    home_page,
    menu_page,
    order_page,
    my_orders,
    order_detail,
    cancel_order,
    complete_order,
    delete_order,
    edit_order,
    invoice_page,
    table_availability,
    reserve_table,
    release_table
    )

# for viewSet List endpoint
menu_item_search = MenuItemSearchViewSet.as_view({'get': 'list'})
menu_item_update = MenuItemViewSet.as_view({
    'put': 'update',
})

urlpatterns = [
    path('', home_page, name='home'),
    path('menu/', menu_page, name='menu'),
    path('order/', order_page, name='order'),
    path('my-orders/', my_orders, name='my_orders'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('order/<int:order_id>/cancel/', cancel_order, name='cancel_order'),
    path('order/<int:order_id>/complete/', complete_order, name='complete_order'),
    path('order/<int:order_id>/edit/', edit_order, name='edit_order'),
    path('order/<int:order_id>/delete/', delete_order, name='delete_order'),
    path('order/<int:order_id>/invoice/', invoice_page, name='invoice_page'),

    path('menu/categories/', MenuCategoryListView.as_view(), name='menu_categories'),
    path('menu/featured-items/', FeaturedMenuItemView.as_view(), name='featured_menu_item'),
    path("menu/items/search/", menu_item_search, name="menu_item_search"),
    path("menu-items/<int:pk>/update", menu_item_update, name="menu_item_update"),
    path("tables/<int:pk>/", TableDetailView.as_view(), name="table_detail"),
    path('api/tables/available/', AvailableTablesAPIView.as_view(), name='available_tables_api'),

    # Table management
    path('tables/', table_availability, name='table_availability'),
    path('tables/<int:table_id>/reserve/', reserve_table, name='reserve_table'),
    path('tables/<int:table_id>/release/', release_table, name='release_table'),
]
