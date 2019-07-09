import json
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.views import status
from .models import Category

User = get_user_model()


# Test Views
class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        user = User.objects.create(username='paddy', email='paddy@mail.com')
        user.set_password('fakepassword')
        user.save()


class AuthRegisterUserTest(BaseViewTest):
    """
    Test for the auth/register/ endpoint
    """
    def test_register_a_user_with_valid_details(self):
        url = reverse(
            "auth-register",
            kwargs={
                "version": "v1"
            }
        )
        response = self.client.post(
            url,
            data=json.dumps({
                "username": "maxwell",
                "password": "password",
                "email": "max@mail.com"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_a_user_with_invalid_data(self):
        url = reverse(
            "auth-register",
            kwargs={
                "version": "v1"
            }
        )
        response = self.client.post(
            url,
            data=json.dumps({
                "username": "",
                "password": "",
                "email": "mail.com"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0], 'This field may not be blank.')
        self.assertEqual(response.data['password'][0], 'This field may not be blank.')
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')

    def test_login_user_with_valid_data(self):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "username": "paddy",
            "password": "fakepassword"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], data['username'])
        self.assertIn("token", response.data)

    def test_login_user_with_invalid_data(self):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "username": "paddington",
            "password": "password"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data['error'], "Invalid Credentials")


# Test Models
class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(category='places')

    def create_category(self, category='games'):
        return Category.objects.create(category=category)

    def test_object_string_representation_is_valid(self):
        category_obj = Category.objects.get(id=1)
        expected_object_name = f'{category_obj.category}'
        self.assertEqual(expected_object_name, str(category_obj))

    def test_category_max_length(self):
        category_name = Category.objects.get(id=1)
        max_length = category_name._meta.get_field('category').max_length
        self.assertEquals(max_length, 100)

    def test_the_category_instance(self):
        category = self.create_category()
        self.assertTrue(isinstance(category, Category))
