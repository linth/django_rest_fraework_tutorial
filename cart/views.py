from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.models import Product

from cart.serializers import ProductSerializer

# https://dev.to/nick_langat/building-a-shopping-cart-using-django-rest-framework-54i0


class ProductAPI(APIView):
    ''' Single API to handle product operations. '''
    serializer_class = ProductSerializer
    
    def get(self, request, fromat=None):
        qs = Product.objects.all()

        return Response(
            {'data': self.serializer_class(qs, many=True).data},
            status=status.HTTP_200_OK
        )
        
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )