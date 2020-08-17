from rest_framework import serializers

from app import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = '__all__'
