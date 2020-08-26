import os
import requests

from rest_framework import generics, mixins, status
from rest_framework.decorators import renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.http import JsonResponse

from app import serializers, models
from app.utils import token


class ProductGenericAPIView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):

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
        try:
            url = os.environ["BASE_URL"] + "/products/register"
        except KeyError:
            url = "https://applifting-python-excercise-ms.herokuapp.com/api/v1/products/register"
        head = {"Bearer": self.my_token}
        response = requests.post(url, data=serializer.data, headers=head)
        if response.status_code == 201:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        if response.status_code == 400:
            token.get_token()
            self.my_token = token.return_token()
            return Response("Offers microservice failed to register a product", status=status.HTTP_400_BAD_REQUEST)
        if response.status_code == 401:
            token.get_token()
            self.my_token = token.return_token()
            return Response("You are not authorised to make this request", status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, product_id):
        return self.update(request, product_id)

    def delete(self, request, product_id):
        return self.destroy(request, product_id)


@renderer_classes((JSONRenderer))
def error404(request, e):
    return JsonResponse({'error': f'{e}: The requested resource was not found on this server'}, status=404)


@renderer_classes((JSONRenderer))
def error400(request, e):
    return JsonResponse({'error': e}, status=400)


@renderer_classes((JSONRenderer))
def error500(request):
    return JsonResponse({'error': 'Internal server error'}, status=500)


@renderer_classes((JSONRenderer))
def error403(request, exception):
    return JsonResponse({'error': exception}, status=403)
