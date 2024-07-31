from django.db import models
from .product import Product
from .cart import Cart

class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product= models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_products')
  