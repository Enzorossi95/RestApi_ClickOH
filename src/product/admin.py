from django.contrib import admin
from .models import Product
# Register your models here.

""""
Se registran los modelos en el admin. (A mi criterio se deberia realizar segun el prpyecto).
"""

admin.site.register(Product)