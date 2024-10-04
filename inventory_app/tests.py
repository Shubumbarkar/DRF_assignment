from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Item

User = get_user_model()

class UserRegistrationTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',  
            'password': 'testpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)

class UserLoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')

    def test_login_user(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

class ItemAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
        login_url = reverse('login')
        response = self.client.post(login_url, {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['tokens']['access']  
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.item_data = {
            'name': 'Test Item',
            'description': 'Test Description',
            'quantity': 5,
            'price': 9.99
        }
        self.item = Item.objects.create(**self.item_data)

    def test_create_item(self):
        url = reverse('create_item')
        response = self.client.post(url, self.item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.item_data['name'])

    def test_read_item(self):
        url = reverse('read_item', kwargs={'item_id': self.item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item_data['name'])

    def test_update_item(self):
        url = reverse('update_item', kwargs={'item_id': self.item.id})
        updated_data = {'name': 'Updated Item', 'description': 'Updated Description', 'quantity': 10, 'price': 12.99}
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_delete_item(self):
        url = reverse('delete_item', kwargs={'item_id': self.item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_read_nonexistent_item(self):
        url = reverse('read_item', kwargs={'item_id': 999})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
