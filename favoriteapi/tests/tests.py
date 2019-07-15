import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

User = get_user_model()


# Test Views
class BaseViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        user = User.objects.create(username='paddy', email='paddy@mail.com')
        user.set_password('fakepassword')
        user.save()
        user1 = User.objects.create(username='pascal', email='pascal@mail.com')
        user1.set_password('fakepassword')
        user1.save()

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
        token = response.data.get("token", '')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def user1_token(self):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "username": "pascal",
            "password": "fakepassword"
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        token1 = response.data.get("token", '')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token1)


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


class FavoriteAPITest(BaseViewTest):
    def test_create_first_favorite_thing_in_category_with_invalid_ranking_fails(self):
        self.user_token()
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "nokia",
            "description": "This is the first of its kind",
            "ranking": 100,
            "category": 1,
            "metadata": {
                "make": 2015,
                "color": "black"
            }
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_favorite_thing_success(self):
        self.user_token()
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "nokia",
            "description": "This is the first of its kind",
            "ranking": 1,
            "category": 1,
            "metadata": {
                "make": 2015,
                "color": "black"
            }
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertIn("created_at", response.data)
        self.assertEqual(response.data['user']['username'], 'paddy')

    def test_create_favorite_thing_in_same_category_success(self):
        self.user_token()
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "motorola",
            "description": "This is the next big thing",
            "ranking": 1,
            "category": 1,
            "metadata": {
                "make": 2019,
                "color": "black"
            }
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_favorite_thing_with_invalid_metadata_fails(self):
        self.user_token()
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "nokia",
            "description": "This is the first of its kind",
            "ranking": 1,
            "category": 1,
            "metadata": {
                "price": 15500.50
            }
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_favorite_thing_with_existing_id_success(self):
        self.user_token()
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "tecno",
            "description": "This is the first of its kind",
            "ranking": 1,
            "category": 1,
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        favorite_id = response.data['id']
        detail_url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite_id
            }
        )
        res = self.client.get(
            detail_url,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], "tecno")

    def test_get_favorite_thing_with_non_existing_id_fails(self):
        self.user_token()
        favorite_id = 1000
        detail_url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite_id
            }
        )
        res = self.client.get(
            detail_url,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data['detail'], "Not found.")

    def test_delete_favorite_thing_success(self):
        self.user_token()
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "oppo",
            "description": "This is the first",
            "ranking": 1,
            "category": 1,
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        favorite_id = response.data['id']
        detail_url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite_id
            }
        )
        res = self.client.delete(
            detail_url,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_favorite_thing_for_a_different_user_fails(self):
        self.user_token()
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "tecno",
            "description": "This is the first of its kind",
            "ranking": 1,
            "category": 1,
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        favorite_id = response.data['id']

        self.user1_token()
        detail_url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite_id
            }
        )
        res = self.client.delete(
            detail_url,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
