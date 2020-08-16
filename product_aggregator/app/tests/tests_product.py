from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from app.tests import factories


class JsonWebToken(APITestCase):
    def tests_no_auth(self):
        response = self.client.get('/product/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tests_auth(self):
        User.objects.create_superuser('matej', 'matej@applifting.cz', 'applifting2020')
        data = {
            "username": "matej",
            "password": "applifting2020"
        }
        response = self.client.post('/api/token/', data=data)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json()["access"])
        response = self.client.get('/product/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductAPI(APITestCase):
    access_token = ''

    def setUp(self):
        User.objects.create_superuser('matej', 'matej@applifting.cz', 'applifting2020')
        data = {
            "username": "matej",
            "password": "applifting2020"
        }
        response = self.client.post('/api/token/', data=data)
        self.access_token = 'Bearer ' + response.json()["access"]

    def tests_404(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.access_token)
        response = self.client.get(f'/product/abc/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tests_create(self):
        data = {
            "name": "Harry Potter",
            "description": "A book about a wizard"
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.access_token)
        response = self.client.post('/product/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tests_update(self):
        product = factories.ProductFactory()
        data = {
            "name": "Harry Potter and the Methods of Rationality",
            "description": "A book about a wizard"
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.access_token)
        response = self.client.put(f'/product/{product.id}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Harry Potter and the Methods of Rationality")

    def tests_delete(self):
        product = factories.ProductFactory()
        self.client.credentials(HTTP_AUTHORIZATION=self.access_token)
        response = self.client.delete(f'/product/{product.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
