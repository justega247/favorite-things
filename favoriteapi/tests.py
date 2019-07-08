from rest_framework.test import APITestCase
# Create your tests here.


class ciTest(APITestCase):
    def test_sum(self):
        assert sum([1, 2, 3]) == 6, "Should be 6"
