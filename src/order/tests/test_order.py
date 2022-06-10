from rest_framework import status

from .test_setup_order import TestOrderSetUp
from .order_factory import OrderFactory
from order.models import Order

"""se van a crear 3 test: 
1) para get ordenes
2) para get orden por id
3) para crear una orden y el detalle.

Se va a utilizar un Order factory que devuelve JSONS o instancias creadas para manipular la base default que 
crean los test.

La clase TestOrder hereda de TestOrderSetUp que tiene el login y el token para la auth de las conusltas a la API.
"""


class TestOrder(TestOrderSetUp):

    def test_get_orders(self):
        order = OrderFactory().create_order_y_detalle()
        response = self.client.get(
            '/orders/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_by_id(self):
        order = OrderFactory().create_order_y_detalle()
        response = self.client.get(
            '/orders/',
            {'id': order.id},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order(self):
        producto = OrderFactory().create_producto()
        order = OrderFactory().build_order_y_detalle_JSON()

        response = self.client.post(
            '/orders/',
            order,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.all().count(), 1)

