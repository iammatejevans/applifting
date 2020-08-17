import requests

from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app import serializers, models
from app.utils import token


class ProductGenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "product_id"
    my_token = token.return_token()

    def get(self, request, product_id=None):
        if product_id:
            return self.retrieve(request, product_id)
        return self.list(request)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        url = 'https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/register'
        head = {
            "Bearer": self.my_token
        }
        response = requests.post(url, data=serializer.data, headers=head)
        if response.status_code == 201:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        elif response.status_code == 400:
            self.my_token = token.get_token()
            return Response(response.json(), status=status.HTTP_400_BAD_REQUEST)
        elif response.status_code == 401:
            self.my_token = token.get_token()
            return Response(response.json(), status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        return self.update(request, product_id)

    def delete(self, request, product_id):
        return self.destroy(request, product_id)
