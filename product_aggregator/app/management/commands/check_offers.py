import requests
import time
from django.core.management.base import BaseCommand
from rest_framework.renderers import JSONRenderer

from app import models, serializers
from app.utils import token


class Command(BaseCommand):
    help = "Test some code"

    def handle(self, *args, **options):
        while True:
            models.Product.objects.create(name="Krtecek", description="a fairytale")
            products = models.Product.objects.all()

            my_token = token.return_token()
            for product in products:
                models.Offer.objects.filter(product=product).delete()
                head = {"Bearer": my_token}
                data = serializers.ProductSerializer(product).data
                json = JSONRenderer().render(data)
                url = f"https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/{product.id}/offers"
                response = requests.get(url, data=json, headers=head)
                if response.status_code == 200:
                    for offer in response.json():
                        a = serializers.OfferSerializer().create(offer)
                        a.product = product
                        a.save()
            time.sleep(60)
