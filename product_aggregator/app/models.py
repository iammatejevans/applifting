import uuid
from django.db import models


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return str(self.name)


class Offer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    price = models.IntegerField(null=True, blank=True)
    items_in_stock = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers")

    def __str__(self):
        return self.product.name + ": " + str(self.price)
