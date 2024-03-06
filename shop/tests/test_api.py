from rest_framework.test import APITestCase
from django.urls import reverse
from shop.models import Product, Category
from shop.serializers import *
from rest_framework import status

class ProductAPITestCase(APITestCase):
    def test_get_list(self):
        category1 = Category.objects.create(name='Категория')
        product1 = Product.objects.create(name='Test1', price=194.5, category=category1)
        product2 = Product.objects.create(name='Test2', price=223.78, category=category1, description='opisanie')
        url = '/shop/api/products'

        response = self.client.get(url)
        serial_data = ProductSerializer([product1, product2], many=True).data

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(serial_data, response.data)


    def test_post_list(self):
        category1 = Category.objects.create(name='Категория')
        product1 = Product(pk=3, name='Test1', price=194.5, category=category1)
        serial_data = ProductSerializer(product1).data

        url = '/shop/api/products'

        response = self.client.post(
            url,
            data={
                'name': 'Test1',
                'price': 194.5,
                'category': category1.pk,
                'exists': True
            }
        )

        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(serial_data.get('name'), response.data.get('name'))