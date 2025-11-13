from django.urls import path
from .views import MenuCategoryListview, FeaturedMenuItemView

urlpatterns = [
    path('menu-categories/',MenuCategoryListview.as_view(),name='menu-categories'),
    path ('featured-item/', FeaturedMenuItemView.as_view(), name='featured-menu-item'),
    
]