from django.urls import path
from .views import UserProfileViewSet, register_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/update/', UserProfileViewSet.as_view({'put': 'update'}), name= 'profile-update'),

]
