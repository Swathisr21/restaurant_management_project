from django.urls import path
from .views import *

urlpatterns = [
    
    path('api/', include('home.urls')),
    
    path('api/orders/', include('orders.urls')),

]