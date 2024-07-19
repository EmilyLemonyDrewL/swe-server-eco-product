from django.db import models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=250)
    product_image = models.CharField(max_length=1000)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=0)

    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value
