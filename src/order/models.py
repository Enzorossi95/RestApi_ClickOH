from sys import path
path.append("../../")
from django.db import models
from product.models import Product

# Create your models here.
"""
Creamos los modelos para Orden y OrderDetail. se validan algunos campos unique, otros auto_now_add para que se 
agrege cuando se crean 

Cada Clave foranea tiene su related_name para relaciones inversas mas faciles de maniobrar mas adelante.

"""


class Order(models.Model):
    number = models.PositiveIntegerField(unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Orden numero {self.number}'


class OrderDetail(models.Model):

    order = models.ForeignKey(Order, related_name='detalle', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(blank=False, default=1)
    product = models.ForeignKey(Product,related_name='product_order_detail', null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Detalle de orden {self.order.number}'
