from django.urls import path
from .views import UserProfileViewSet

urlpatterns = [
    path('profile/update/', UserProfileViewSet.as_view({'put': 'updated'}), name= 'profile-update'),
    
]