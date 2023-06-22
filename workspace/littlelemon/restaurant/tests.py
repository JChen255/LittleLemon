from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer
from django.contrib.auth.models import User


class MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title="Avocado Toast", price=13.5, inventory=50)
        self.assertEqual(str(item), "Avocado Toast : 13.5")

class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
            # Create test instances of Menu model
        Menu.objects.create(title="Avocado Toast", price=13.5, inventory=50)
        Menu.objects.create(title="Smoked Salmon", price=14.5, inventory=100)
        Menu.objects.create(title="Ahi Tuna Bites", price=15.5, inventory=60)
        Menu.objects.create(title="Chili Chesseburger", price=16.5, inventory=55)

    def test_getall(self):
        # Make GET request to retrieve all Menu objects
        url = reverse('menu')
        response = self.client.get(url)

        # Retrieve all Menu objects from the database
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)

        # Compare serialized data with the response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class MenuViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        Menu.objects.create(title="Avocado Toast", price=13.5, inventory=50)
        Menu.objects.create(title="Smoked Salmon", price=14.5, inventory=100)
        Menu.objects.create(title="Ahi Tuna Bites", price=15.5, inventory=60)
        Menu.objects.create(title="Chili Chesseburger", price=16.5, inventory=55)

    def test_getall(self):
        url = reverse('menu')

        # Fetch the data from the API
        response = self.client.get(url)

        # Make sure the status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Fetch the data from the database
        menu_items = Menu.objects.all()
        serializer = MenuSerializer(menu_items, many=True)

        # Make sure the data matches
        self.assertEqual(response.data, serializer.data)