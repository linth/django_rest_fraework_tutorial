from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cart.models import Product

from cart.serializers import ProductSerializer
from cart.service import Cart

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
    

class CartAPI(APIView):

    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {'data': list(cart.__iter__()),
             'cart_total_price': cart.get_total_price()},
             status=status.HTTP_200_OK
        )
    
    def post(self, request, **kwargs):
        cart = Cart(request)

        if 'remove' in request.data:
            product = request.data['product']
            cart.remove(product)
        elif 'clear' in request.data:
            cart.clear()
        else:
            product = request.data
            cart.add(product=product['product'],
                     quantity=product['quantity'],
                     overide_quantity=product['overide_quantity'] if 'overide_quantity' in product else False
                     )

        return Response(
            {'message': 'cart update'},
            status=status.HTTP_202_ACCEPTED
        )