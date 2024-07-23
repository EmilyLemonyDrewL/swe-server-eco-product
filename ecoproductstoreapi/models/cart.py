from django.db import models
from .user import User
from .product import Product

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity= models.IntegerField(default=1)
