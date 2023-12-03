from django.urls import path
from snippets import views

from cart.views import ProductAPI

urlpatterns = [
    path('products/', ProductAPI.as_view(), name='products'),
]