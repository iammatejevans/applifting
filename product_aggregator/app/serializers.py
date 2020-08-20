from rest_framework import serializers

from app import models


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = ["id", "price", "items_in_stock"]


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    description = serializers.CharField()
    offers = OfferSerializer(many=True, allow_null=True, required=False)

    def create(self, validated_data):
        return models.Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.name)
        instance.save()
        return instance

    class Meta:
        model = models.Product
        fields = ["id", "name", "description", "offers"]
