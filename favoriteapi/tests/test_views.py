import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from ..models import Category, Favorite


User = get_user_model()


# Test Views
class BaseViewTest(APITestCase):
    client = APIClient()

    category1 = Category.objects.create(category='phones')

    def setUp(self):
        user = User.objects.create(username='paddy', email='paddy@mail.com')
        user.set_password('fakepassword')
        user.save()
        user1 = User.objects.create(username='pascal', email='pascal@mail.com')
        user1.set_password('fakepassword')
        user1.save()

    def user_token(self, data):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        data = data
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        token = response.data.get("token", '')
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def create_favorite(self,
                        user,
                        metadata,
                        title='tecno',
                        description='This is just a china phone',
                        ranking=1,
                        category=category1):
        user = user
        metadata = metadata
        return Favorite.objects.create(
            title=title,
            description=description,
            ranking=ranking,
            metadata=metadata,
            user=user,
            category=category)


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
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
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

    def test_get_categories_where_user_has_favorites(self):
        user = User.objects.filter(username='paddy').first()
        favorite = self.create_favorite(user=user, metadata={"size": "medium"})
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
        url = reverse(
            "category-list",
            kwargs={
                "version": "v1"
            }
        )
        response = self.client.get(
            url,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['category'], 'phones')


class FavoriteAPITest(BaseViewTest):
    def test_create_first_favorite_thing_in_category_with_invalid_ranking_fails(self):
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
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
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
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
        user = User.objects.filter(username='paddy').first()
        favorite = self.create_favorite(user=user, metadata={"size": "medium"})
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
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
            "category": 2,
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
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
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
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
        user = User.objects.filter(username='paddy').first()
        favorite = self.create_favorite(user=user, metadata={"size": "medium"})
        detail_url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite.id
            }
        )
        res = self.client.get(
            detail_url,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], "tecno")

    def test_get_favorite_thing_with_non_existing_id_fails(self):
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
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
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
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
        user = User.objects.filter(username='pascal').first()
        favorite = self.create_favorite(user=user, metadata={"size": "medium"})
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
        detail_url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite.id
            }
        )
        res = self.client.delete(
            detail_url,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_favorite_thing_success(self):
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "xiaoming",
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
        data = {
            "metadata": {
                "color": "black"
            }
        }
        res = self.client.patch(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("color", res.data["metadata"])

    def test_update_favorite_thing_ranking_success(self):
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "xiaoming",
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
        current_ranking = response.data['ranking']

        detail_url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite_id
            }
        )
        data = {
            "ranking": 2
        }
        res = self.client.patch(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['message'], f'The highest ranking you can update to at the moment is {current_ranking}')

    def test_update_favorite_thing_with_invalid_ranking_fails(self):
        self.user_token(
            data={
                "username": "paddy",
                "password": "fakepassword"
            })
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "xiaoming",
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
        data = {
            "ranking": -2
        }
        res = self.client.patch(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['message'], 'Sorry your ranking has to be a positive integer')

    def test_update_existing_favorite_ranking_in_a_category_success(self):
        user = User.objects.filter(username='pascal').first()
        favorite = self.create_favorite(user=user, metadata={"size": "medium"})
        self.user_token(
            data={
                "username": "pascal",
                "password": "fakepassword"
            })
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "xiaoming",
            "description": "This is the first of its kind",
            "ranking": 2,
            "category": 2,
        }
        self.client.post(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        detail_url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite.id
            }
        )
        data = {
            "title": "joker",
            "ranking": 2
        }
        res = self.client.patch(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_existing_favorite_ranking_to_a_lower_value_in_a_category_success(self):
        user = User.objects.filter(username='pascal').first()
        favorite = self.create_favorite(user=user, metadata={"size": "medium"})
        self.user_token(
            data={
                "username": "pascal",
                "password": "fakepassword"
            })
        url = reverse(
            "create-favorite",
            kwargs={
                "version": "v1"
            }
        )
        data = {
            "title": "xiaoming",
            "description": "This is the first of its kind",
            "ranking": 2,
            "category": 2,
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
        data = {
            "title": "joker",
            "ranking": 1
        }
        res = self.client.patch(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_favorite_things_under_a_category_success(self):
        user = User.objects.filter(username='pascal').first()
        favorite = self.create_favorite(user=user, metadata={"size": "medium"})
        self.user_token(
            data={
                "username": "pascal",
                "password": "fakepassword"
            })
        url = reverse(
            "favorite-category-list",
            kwargs={
                "version": "v1",
                "category_id": 2
            }
        )
        res = self.client.get(
            url,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)


class AuditViewTest(BaseViewTest):
    def test_favorite_thing_audit_log_is_tracked_success(self):
        user = User.objects.filter(username='pascal').first()
        favorite = self.create_favorite(user=user, metadata={"size": "medium"})
        favorite_id = favorite.id
        self.user_token(
            data={
                "username": "pascal",
                "password": "fakepassword"
            })
        url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite_id
            }
        )
        data = {
            "title": "xiaoming",
            "description": "This is the first of its kind",
            "ranking": 1
        }
        self.client.patch(
            url,
            data=json.dumps(data),
            content_type="application/json"
        )
        audit_url = reverse(
            "favorite-history",
            kwargs={
                "version": "v1",
                "id": favorite.id
            }
        )
        res = self.client.get(
            audit_url,
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("audit", res.data)
        self.assertIn('title changed from tecno to xiaoming', res.data["audit"])