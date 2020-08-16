import factory
from faker import Faker
from app import models

fake = Faker()
# noqa pylint: disable=E1101


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Product

    name = fake.name()
    description = fake.text()


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Offer

    price = fake.pyint()
    items_in_stock = fake.pyint()
    product = factory.SubFactory(ProductFactory)
