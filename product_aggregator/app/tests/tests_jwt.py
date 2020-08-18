from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class JsonWebToken(APITestCase):
    def tests_no_auth(self):
        response = self.client.get("/product/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tests_auth(self):
        User.objects.create_superuser("matej", "matej@applifting.cz", "applifting2020")
        data = {"username": "matej", "password": "applifting2020"}
        response = self.client.post("/api/token/", data=data)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.json()["access"])
        response = self.client.get("/product/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
