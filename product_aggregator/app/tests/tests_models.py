from rest_framework.test import APITestCase
from app.tests import factories
from app import models


class ProductModel(APITestCase):
    def tests_create(self):
        product = models.Product.objects.create(name="Harry Potter", description="A book about a wizard")
        self.assertEqual(models.Product.objects.all().count(), 1)
        get_product = models.Product.objects.get(id=product.id)
        self.assertEqual(get_product.name, product.name)
        self.assertEqual(get_product.description, product.description)

    def tests_update(self):
        product = models.Product.objects.create(name="Harry Potter", description="A book about a wizard")
        product.name = "Harry Potter and the Methods of Rationality"
        product.save()
        self.assertEqual(models.Product.objects.all().count(), 1)
        get_product = models.Product.objects.get(id=product.id)
        self.assertEqual(get_product.name, "Harry Potter and the Methods of Rationality")
        self.assertEqual(get_product.description, product.description)

    def tests_get(self):
        for _ in range(5):
            factories.ProductFactory()
        products = models.Product.objects.all()
        self.assertEqual(products.count(), 5)

    def tests_delete(self):
        product = factories.ProductFactory()
        self.assertEqual(models.Product.objects.all().count(), 1)
        product.delete()
        self.assertEqual(models.Product.objects.all().count(), 0)


class OfferModel(APITestCase):
    def tests_create(self):
        product = factories.ProductFactory()
        offer = models.Offer.objects.create(price=159, items_in_stock=12, product=product)
        factories.OfferFactory()
        self.assertEqual(models.Offer.objects.all().count(), 2)
        self.assertEqual(models.Offer.objects.filter(product=product).count(), 1)
        self.assertEqual(models.Offer.objects.get(product=product).price, offer.price)
        self.assertEqual(models.Offer.objects.get(product=product).items_in_stock, offer.items_in_stock)

    def tests_update(self):
        offer = factories.OfferFactory(items_in_stock=42)
        offer.items_in_stock -= 1
        offer.save()
        self.assertEqual(models.Offer.objects.all().count(), 1)
        self.assertEqual(models.Offer.objects.get(id=offer.id).items_in_stock, 41)

    def tests_get(self):
        product = factories.ProductFactory()
        for _ in range(5):
            factories.OfferFactory(product=product)
        self.assertEqual(models.Offer.objects.filter(product=product).count(), 5)

    def tests_delete(self):
        offer = factories.OfferFactory()
        self.assertEqual(models.Offer.objects.all().count(), 1)
        offer.delete()
        self.assertEqual(models.Offer.objects.all().count(), 0)