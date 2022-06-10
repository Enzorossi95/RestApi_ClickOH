import requests
from product.models import Product

"""
Modulo UTILS para herramientas que luego utilizaremos en los serializers y vistas. 

Por lo general me interesa tener estos metodos herramientas en difrentes archivos para excalrecer el codigo.
"""


def valor_actual_dolar_blue_venta():
    URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
    r = requests.get(url=URL)
    data = r.json()
    dolar_blue = next(iter(item['casa']['venta'] for item in data if item['casa']['nombre'] == 'Dolar Blue'), None).replace(',', '.')
    return float(dolar_blue)


def decrease_stock(order_detail):
    producto_en_la_base = Product.objects.get(id=order_detail['product'].id)
    producto_en_la_base.stock -= order_detail['quantity']
    producto_en_la_base.save()
    return True


def add_stock(order_detail):
    producto_en_la_base = Product.objects.get(id=order_detail.product.id)
    producto_en_la_base.stock += order_detail.quantity
    producto_en_la_base.save()
    return True


def update_stock_sumar_diferencia(order_detail, stock_a_agregar):
    producto_en_la_base = Product.objects.get(id=order_detail.product.id)
    producto_en_la_base.stock += stock_a_agregar
    producto_en_la_base.save()
    return True


def update_stock_restar_diferencia(order_detail, stock_a_agregar):
    producto_en_la_base = Product.objects.get(id=order_detail.product.id)
    producto_en_la_base.stock -= stock_a_agregar
    producto_en_la_base.save()
    return True
