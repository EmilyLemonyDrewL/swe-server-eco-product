from django.db import models
from .user import User
from .product import Product

class Cart(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.IntegerField(default=0, blank=True)
