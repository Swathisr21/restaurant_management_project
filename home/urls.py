from django.urls import path
from .views import (MenuCategoryListview, FeaturedMenuItemsView, MenuItemSearchViewset, MenuItemIngredientsView)

menu_item_search = MenuItemSearchViewset.as_view({'get': 'list'})

urlpatterns = [
    path('menu/categories/',MenuCategoryListview.as_view(),name='menu_categories'),
    path('menu/featured-items/', FeaturedMenuItemsView.as_view(), name='featured_menu_item'),
    path("menu/items/search/", menu_item_search, name="menu_item_search"), 
    path("menu/items/<int:pk>/ingredients/", MenuItemIngredientsView.as_view(), name="menu_item_ingredients"),
]