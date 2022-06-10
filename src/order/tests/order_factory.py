from faker import Faker
from order.models import Order, OrderDetail
from product.models import Product

"""
Este modulo se utiliza para crear JSON y Objetos en la base para maniobrar los TEST.

Se utiliza Faker, una libreria externa para generar contenido "FAKE" en la base
"""

faker = Faker()

class OrderFactory:
    def build_order_JSON(self):
        return {
            'number': faker.random_number(digits=2),
        }

    def build_producto_JSON(self):
        return {
            'id': 'producto1',
            'name': 'camisa',
            'price': 25.2,
            'stock': 45
        }

    def build_order_detail_JSON(self):
        return {
            'product_id': 'producto1',
            'quantity': 1
        }

    def build_order_y_detalle_JSON(self):

        return {
            'number': 3,
            'detalle': [
                {
                    "quantity": 1,
                    "product": "producto1"
                }
            ]

        }

    def create_producto(self):
        return Product.objects.create(**self.build_producto_JSON())

    def create_order_y_detalle(self):
        producto = Product.objects.create(**self.build_producto_JSON())
        orden = Order.objects.create(number=2)
        OrderDetail.objects.create(order=orden, product_id='producto1', quantity= 1)
        return orden
