from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Category, Favorite

User = get_user_model()


# Test Models
class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(category='places')

    def create_category(self, category='games'):
        return Category.objects.create(category=category)

    def test_object_string_representation_for_category_is_valid(self):
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


class FavoriteModelTest(TestCase):

    user1 = User.objects.create(username='passo', email='pass@mail.com', password='extended')
    category1 = Category.objects.create(category='phones')
    data = {"size": "medium"}

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(username='paulo', email='paulo@mail.com', password='extended')
        category1 = Category.objects.create(category='phones')
        data = {"size": "medium"}
        Favorite.objects.create(
            title='tecno',
            description='This is just a china phone',
            ranking=1,
            metadata=data,
            user=user1,
            category=category1)

    def create_favorite(self,
                        title='tecno',
                        description='This is just a china phone',
                        ranking=1,
                        metadata=data,
                        user=user1,
                        category=category1):
        return Favorite.objects.create(
            title=title,
            description=description,
            ranking=ranking,
            metadata=metadata,
            user=user,
            category=category)

    def test_the_favorite_instance(self):
        favorite = self.create_favorite()
        self.assertTrue(isinstance(favorite, Favorite))

    def test_object_string_representation_for_favorite_is_valid(self):
        favorite_obj = Favorite.objects.get(id=1)
        expected_object_name = f'{favorite_obj.title}'
        self.assertEqual(expected_object_name, str(favorite_obj))
