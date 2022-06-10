from django.contrib import admin
from .models import Order, OrderDetail

""""
Se registran los modelos en el admin. (A mi criterio se deberia realizar segun el prpyecto).
"""


# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetail)