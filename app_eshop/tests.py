from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Person, Product

"""
Sentencias para pruebas reales:

INSERT INTO app_eshop_person(name, email) VALUES
('Pepe', 'pepe@gmail.com'),
('Antonio', 'antonio@gmail.com');

INSERT INTO app_eshop_product(name, stock) VALUES
('Mesa', 4),
('Silla', 5);
"""


class PersonViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.person_data_1 = {
            'name': 'Rocio',
            'email': 'r@r.com',
        }
        self.person_data_2 = {
            'name': 'Jose',
            'email': 'a@a.com',
        }

        self.person_1 = Person.objects.create(**self.person_data_1)
        self.person_2 = Person.objects.create(**self.person_data_2)

        self.product_data_1 = {
            'name': 'Mesa',
            'stock': 4,
        }
        self.product_data_2 = {
            'name': 'Silla',
            'stock': 5,
        }

        self.product_1 = Product.objects.create(**self.product_data_1)
        self.product_2 = Product.objects.create(**self.product_data_2)

    def test_get_all_people(self):
        response = self.client.get(reverse('people-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        people = response.json()
        self.assertEqual(len(people), 2)

    def test_get_all_products(self):
        response = self.client.get(reverse('products-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        products = response.json()
        self.assertEqual(len(products), 2)

    def test_people_search_ok(self):
        url = reverse('people-search')

        response = self.client.get(url + '?query=Rocio')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        people = response.json()
        self.assertEqual(len(people['results']), 1)

        person = people['results'][0]
        self.assertEqual(person['id'], self.person_1.id)
        self.assertEqual(person['name'], self.person_1.name)
        self.assertEqual(person['email'], self.person_1.email)

    def test_people_search_without_query_error(self):
        response = self.client.get(reverse('people-search'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_products_search_ok(self):
        url = reverse('products-search')

        response = self.client.get(url + '?query=silla')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        products = response.json()
        self.assertEqual(len(products['results']), 1)

        product = products['results'][0]
        self.assertEqual(product['id'], self.product_2.id)
        self.assertEqual(product['name'], 'Silla')
        self.assertEqual(product['stock'], 5)

    def test_products_search_without_query_error(self):
        response = self.client.get(reverse('products-search'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_single_person(self):
        response = self.client.get(reverse('people-detail', kwargs={'pk': self.person_2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_single_product_not_found(self):
    #     response = self.client.get(reverse('products-detail', kwargs={'pk': 'a-nonexistent-uuid'}))
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_purchase_ok(self):
        url = reverse('cart-list')
        data = {
            'productId': str(self.product_1.id),
            'quantity': 3,
            'email': self.person_1.email,
        }
        response = self.client.post(url, data)

        purchased_item = self.person_1.purchased_items.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(purchased_item.product, self.product_1)
        self.assertEqual(purchased_item.person, self.person_1)
        self.assertEqual(purchased_item.quantity, 3)

    def test_purchase_not_found_product_error(self):
        url = reverse('cart-list')
        data = {
            'productId': 3,
            'quantity': 6,
            'email': self.person_1.email,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        error = response.json()
        self.assertEqual(error['detail'], 'Producto no encontrado')

    def test_purchase_not_found_person_error(self):
        url = reverse('cart-list')
        data = {
            'productId': str(self.product_1.id),
            'quantity': 6,
            'email': 'manolo@gmail.com'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        error = response.json()
        self.assertEqual(error['detail'], 'Persona no encontrada')

    def test_purchase_not_enough_stock_error(self):
        url = reverse('cart-list')
        data = {
            'productId': str(self.product_1.id),
            'quantity': 6,
            'email': self.person_1.email,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = response.json()
        self.assertEqual(error['detail'], 'Stock insuficiente para el producto')

