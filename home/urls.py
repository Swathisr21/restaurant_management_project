from django.urls import path, include
from .views import (
    MenuCategoryListview, 
    FeaturedMenuItemsView, 
    MenuItemSearchViewset, 
    MenuItemIngredientsView,
    MenuItemViewSet,
    TableDetailView,
    AvailableTablesAPIView,
    MenuItemViewSet,
    MenuItemReviewViewSet,
    MenuCategoryViewSet,
    RestaurantInfoView
    )
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    "categories",
    MenuCategoryViewSet,
    basename="menu-category"
)

# for viewSet List endpoint
menu_item_search = MenuItemSearchViewset.as_view({'get': 'list'})
menu_item_update = MenuItemViewSet.as_view({
    'put': 'update',
})

router = DefaultRouter()
router.register('menu-categories', MenuCategoryViewSet, basename='menu-category')

urlpatterns = [
    path('menu/categories/', MenuCategoryListview.as_view(),name='menu_categories'),
    path('menu/featured-items/', FeaturedMenuItemsView.as_view(), name='featured_menu_item'),
    path("menu/items/search/", menu_item_search, name="menu_item_search"), 
    path("menu/items/<int:pk>/ingredients/", MenuItemIngredientsView.as_view(), name="menu_item_ingredients"),
    path("menu-items/<int:pk>/update", menu_item_update, name="menu_item_update"),
    path("tables/<int:pk>/", TableDetailView.as_view(), name="table_detail"),
    path('api/tables/available/', AvailableTablesAPIView.as_view(), name='available_tables_api'),
    path('daily-specials/', DailySpecialsView.as_view(), name="daily-specials"),
    path("", include(router.urls)),
    path("reviews/create/", CreateUserReviewView.as_view()),
    path("menu-items/<int:menu_item_id>/reviews/", MenuItemReviewViewSet.as_view(), name="menu-item-reviews"),
    path("restaurant/info/", RestaurantInfoView.as_view(), name="restaurant-info"),

]

