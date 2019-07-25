import json
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from ..models import Category, Favorite


# Test Views
class BaseViewTest(APITestCase):
    client = APIClient()

    category1 = Category.objects.create(category='phones')

    def create_favorite(self,
                        metadata,
                        title='tecno',
                        description='This is just a china phone',
                        ranking=1,
                        category=category1):
        metadata = metadata
        return Favorite.objects.create(
            title=title,
            description=description,
            ranking=ranking,
            metadata=metadata,
            category=category)


class CategoryAPITest(BaseViewTest):
    def test_create_category_success(self):
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
        self.assertEqual(response.data['category'], data['category'].upper())


class FavoriteAPITest(BaseViewTest):
    def test_create_first_favorite_thing_in_category_with_invalid_ranking_fails(self):
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
        self.assertIn("created_at", response.data)

    def test_create_favorite_thing_in_same_category_success(self):
        favorite = self.create_favorite(metadata={"size": "medium"})
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
        favorite = self.create_favorite(metadata={"size": "medium"})
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

    def test_update_favorite_thing_success(self):
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
            "title": "tecno",
            "ranking": 1,
            "category": 1,
            "metadata": {
                "color": "black"
            }
        }
        res = self.client.put(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("color", res.data["metadata"])

    def test_update_favorite_thing_ranking_to_value_larger_than_the_max_fails(self):
        favorite = self.create_favorite(metadata={"size": "medium"})
        # url = reverse(
        #     "create-favorite",
        #     kwargs={
        #         "version": "v1"
        #     }
        # )
        # data = {
        #     "title": "xiaoming",
        #     "description": "This is the first of its kind",
        #     "ranking": 1,
        #     "category": 1,
        # }
        # response = self.client.post(
        #     url,
        #     data=json.dumps(data),
        #     content_type="application/json"
        # )
        favorite_id = favorite.id
        current_ranking = favorite.ranking

        detail_url = reverse(
            "detail-favorite",
            kwargs={
                "version": "v1",
                "id": favorite_id
            }
        )
        data = {
            "title": "tecno",
            "ranking": 3,
            "category": 1,
            "metadata": {
                "color": "black"
            }
        }
        res = self.client.put(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['message'], f'The highest ranking you can update to at the moment is {current_ranking}')

    def test_update_favorite_thing_with_invalid_ranking_fails(self):
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
        res = self.client.put(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data['message'], 'Sorry your ranking has to be a positive integer')

    def test_update_existing_favorite_ranking_in_a_category_success(self):
        favorite = self.create_favorite(metadata={"size": "medium"})
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
            "title": "xiaoming",
            "description": "This is the first of its kind",
            "ranking": 1,
            "category": 2,
        }
        res = self.client.put(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['description'], data['description'])

    def test_update_existing_favorite_ranking_to_a_lower_value_in_a_category_success(self):
        favorite = self.create_favorite(metadata={"size": "medium"})
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
            "title": "xiaoming",
            "description": "This is the first of its kind",
            "ranking": 1,
            "category": 1,
        }
        res = self.client.put(
            detail_url,
            data=json.dumps(data),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_favorite_things_under_a_category_success(self):
        favorite = self.create_favorite(metadata={"size": "medium"})
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


class AuditViewTest(BaseViewTest):
    def test_favorite_thing_audit_log_is_tracked_success(self):
        favorite = self.create_favorite(metadata={"size": "medium"})
        favorite_id = favorite.id
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
            "ranking": 1,
            "category": 2
        }
        self.client.put(
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
