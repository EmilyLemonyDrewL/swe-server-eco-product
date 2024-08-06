from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ecoproductstoreapi.models import Product, Category

class ProductViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")
        self.product_data = {
            "name": "Test Product",
            "price": 9.99,
            "description": "A test product",
            "product_image": "test_image.jpg",
        }
        self.product = Product.objects.create(**self.product_data, category=self.category)

    def test_retrieve_product(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product_data['name'])

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        url = reverse('product-list')
        new_product_data = self.product_data.copy()
        new_product_data['name'] = "New Test Product"
        new_product_data['category'] = self.category.id
        response = self.client.post(url, new_product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_update_product(self):
        url = reverse('product-detail', args=[self.product.id])
        updated_data = self.product_data.copy()
        updated_data['name'] = "Updated Test Product"
        updated_data['category'] = self.category.id
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Test Product")

    def test_delete_product(self):
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_in_cart_action(self):
        self.product.joined = False
        self.product.joined = not self.product.joined
        self.assertTrue(self.product.joined)
        self.product.joined = not self.product.joined
        self.assertFalse(self.product.joined)



    def test_by_category_action(self):
        url = reverse('product-by-category')
        response = self.client.get(url, {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
