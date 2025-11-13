from django.urls import path
from .views import MenuCategoryListview, FeaturedMenuItemsView

urlpatterns = [
    path('menu-categories/',MenuCategoryListview.as_view(),name='menu_categories'),
    path ('featured-items/', FeaturedMenuItemsView.as_view(), name='featured_menu_item'),
    
]