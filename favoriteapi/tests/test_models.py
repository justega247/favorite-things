from django.test import TestCase
from ..models import Category


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
