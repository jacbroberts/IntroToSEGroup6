from django.test import TestCase
from django.urls import reverse

class ReturnProductTest(TestCase):
    def test_return_product_view(self):
        response = self.client.get(reverse('return_product'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Return Product")

    def test_return_success_view(self):
        response = self.client.get(reverse('return_success'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Product returned successfully!")
