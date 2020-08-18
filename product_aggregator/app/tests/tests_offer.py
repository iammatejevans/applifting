import requests

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from app.tests import factories
from app.utils import token
from app import serializers, models


class OfferAPI(APITestCase):
    json_web_token = ""

    def setUp(self):
        User.objects.create_superuser("matej", "matej@applifting.cz", "applifting2020")
        data = {"username": "matej", "password": "applifting2020"}
        response = self.client.post("/api/token/", data=data)
        self.json_web_token = "Bearer " + response.json()["access"]

    def tests_no_auth(self):
        product = factories.ProductFactory()
        data = serializers.ProductSerializer(product).data
        url = "https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/register/"
        response = requests.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        head = {"Bearer": "abc"}
        response = requests.post(url, data=data, headers=head)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tests_create(self):
        data = {"name": "Harry Potter", "description": "A book about a wizard"}
        self.client.credentials(HTTP_AUTHORIZATION=self.json_web_token)
        response = self.client.post("/product/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        product = models.Product.objects.get(name="Harry Potter")

        url = "https://applifting-python-excercise-ms.herokuapp.com/api/v1/auth"
        response = requests.post(url)
        access_token = response.json()["access_token"]

        url = "https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/register"
        head = {"Bearer": access_token}
        response = requests.post(url, data=serializers.ProductSerializer(product).data, headers=head)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["id"], str(product.id))

        url = f"https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/{product.id}/offers"
        response = requests.get(url, headers=head)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tests_404(self):
        product = factories.ProductFactory()
        access_token = token.return_token()
        head = {"Bearer": access_token}
        url = f"https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/{product.id}/offers"
        response = requests.get(url, headers=head)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
