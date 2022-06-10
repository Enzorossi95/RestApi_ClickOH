from django.db import models

# Create your models here.
"""
Creamos los modelos para Producto. se validan algunos campos unique, otros auto_now_add para que se 
agrege cuando se crean 

Cada Clave foranea tiene su related_name para relaciones inversas mas faciles de maniobrar mas adelante.

"""

class Product(models.Model):
    id = models.CharField('id', max_length=255, primary_key=True)
    name = models.CharField('nombre del producto', max_length=255, blank=False, null=False)
    price = models.FloatField('precio del producto', blank=False, null=False, default=0.00)
    stock = models.IntegerField('Stock del producto', blank=False, null=False, default=0)

    def __str__(self):
        """Retornamos nombre y precio para str general"""
        return f'Producto: {self.name} | {self.price}'

    @property
    def get_price(self):
        """Returns precio del prodcuto"""
        return f'{self.price}'

    class Meta:
        ordering = ["id"]
