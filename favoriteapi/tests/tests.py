import json
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.views import status

User = get_user_model()


# Test Views
class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        user = User.objects.create(username='paddy', email='paddy@mail.com')
        user.set_password('fakepassword')
        user.save()


class AuthUserAPITest(BaseViewTest):
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


class CategoryAPITest(BaseViewTest):
    def user_token(self):
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
        token = response.data.get("token", 0)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def test_create_category_success(self):
        self.user_token()
        url = reverse(
            "category-list",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "category": "gaMes"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], data['category'].lower())

    def test_create_category_without_token_fails(self):
        url = reverse(
            "category-list",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "category": "places"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
