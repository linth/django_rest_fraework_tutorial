from django.urls import path
from snippets import views

from cart.views import ProductAPI, CartAPI

urlpatterns = [
    path('products/', ProductAPI.as_view(), name='products'),
    path('cart/', CartAPI.as_view(), name='cart'),
]