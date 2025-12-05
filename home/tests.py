from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from .models import Restaurant


class RestaurantInfoAPITest(APITestCase):
    def test_get_restaurant_info(self):
        # a. Create a sample Restaurant instance
        restaurant = Restaurant.objects.create(
            name='Test Restaurant',
            address='123 Test St'
        )

        # b. Make GET request to the API
        response = self.client.get('/api/restaurant-info/')
        # Change this URL if your actual endpoint is different

        # c. Assert status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # d. Assert response data matches created Restaurant
        self.assertEqual(response.data['name'], restaurant.name)
        self.assertEqual(response.data['address'], restaurant.address)
        