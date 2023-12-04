from django.conf import settings
from .serializers import ProductSerializer
from .models import Product
from decimal import Decimal


class Cart:

    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an emptycart in session.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, overide_quantity=False):
        ''' add product to the cart or update its quantity. '''
        product_id = str(product['id'])
        if product_id not in self.cart:
            self.cart[product_id] = {

            }
        if overide_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        ''' remove a product from the cart. '''
        product_id = str(product['id'])

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        ''' loop through cart items and fetch the products from the database. '''
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = ProductSerializer(product).data
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        ''' count all items in the cart. '''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        