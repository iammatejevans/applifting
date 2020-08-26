import os
import requests

from django.core.management.base import BaseCommand
from rest_framework.renderers import JSONRenderer

from app import models, serializers
from app.utils import token


class Command(BaseCommand):
    help = "Check for offers for each product. To by run by a task scheduler."

    def handle(self, *args, **options):
        products = models.Product.objects.all()
        my_token = token.return_token()

        try:
            url = os.environ["BASE_URL"] + "/products/register"
        except KeyError:
            url = "https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/register"

        for product in products:
            models.Offer.objects.filter(product=product).delete()
            head = {"Bearer": my_token}
            data = serializers.ProductSerializer(product).data
            json = JSONRenderer().render(data)
            response = requests.get(url, data=json, headers=head)
            if response.status_code == 200:
                for offer in response.json():
                    a = serializers.OfferSerializer().create(offer)
                    a.product = product
                    a.save()
