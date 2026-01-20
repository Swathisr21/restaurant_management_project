from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Order, OrderStatus, Contact


class RestaurantAPITestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create order status
        self.pending_status = OrderStatus.objects.create(name='pending')
        self.completed_status = OrderStatus.objects.create(name='completed')

    def test_contact_form_api(self):
        """Test contact form API creation"""
        self.client.force_authenticate(user=self.user)

        contact_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }

        response = self.client.post('/api/orders/contact/', contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.first().name, 'Test User')

    def test_order_history_api(self):
        """Test order history API"""
        self.client.force_authenticate(user=self.user)

        # Create a test order
        order = Order.objects.create(
            user=self.user,
            customer_name='Test Customer',
            status=self.pending_status
        )

        response = self.client.get('/api/orders/order/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['customer_name'], 'Test Customer')

    def test_user_profile_update_api(self):
        """Test user profile update API"""
        self.client.force_authenticate(user=self.user)

        profile_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }

        response = self.client.put('/accounts/profile/update/', profile_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)

        # Refresh user from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
