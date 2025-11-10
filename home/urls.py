from django.urls import path
from .views import MenuCategoryListview

urlpatterns = [
    path('menu-categories/',MenuCategoryListview.as_view(),name='menu-categories'),

    
]