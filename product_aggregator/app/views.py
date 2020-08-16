from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from app import serializers, models


class ProductGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "product_id"

    def get(self, request, product_id=None):
        if product_id:
            return self.retrieve(request, product_id)
        return self.list(request)

    def post(self, request):
        # TODO: call offers microservice to register new product
        return self.create(request)

    def put(self, request, product_id):
        return self.update(request, product_id)

    def delete(self, request, product_id):
        return self.destroy(request, product_id)
