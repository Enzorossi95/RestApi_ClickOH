from django.db import transaction
from rest_framework import serializers
from ..models import Order, OrderDetail
from ..utils import decrease_stock, add_stock, update_stock_sumar_diferencia, update_stock_restar_diferencia
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from product.models import Product
from collections import Counter


""""
Serializers, archivo corazon de la app Order, aqui vamos a crear los nested objects entre Order y DEtailOrder para
tener en la misma ruta la creacion,detalle y listado de orden con su detalle.

"""


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['id', 'quantity', 'product']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False}
        }

    def validate_quantity(self, value):
        if value <= 0 or value is None:
            raise serializers.ValidationError('La cantidad debe ser mayor a 0.')
        else:
            return value


class OrderSerializer(serializers.ModelSerializer):

    detalle = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def validate_detalle(self,value):
        productos_sin_stock = []
        """
        Cabe aclarar que se podria realizar de diferentes maneras, dejo comentado un list comprehension que utilice pero luego decidi 
        desglosar para una mejor compresion de lectura del codigo.
        
        # productos_sin_stock = [Product.objects.get(pk=k['product'].id) for k in value if k['quantity'] > Product.objects.get(pk=k['product'].id).stock]
        """
        for k in value:
            producto_en_la_base = Product.objects.get(id=k['product'].id)
            if k['quantity'] > producto_en_la_base.stock:
                productos_sin_stock.append(producto_en_la_base.id)
        array_de_productos = [d['product'] for d in value]
        duplicate_values = [k for k, v in Counter(array_de_productos).items() if v > 1]
        if len(duplicate_values) > 0:
            raise serializers.ValidationError(f'hay productos repetidos en la orden: {duplicate_values}')
        elif len(productos_sin_stock) > 0:
            raise serializers.ValidationError(f'hay productos sin stock: {productos_sin_stock}')
        else:
            return value

    def create(self, validated_data):
        details_data = validated_data.pop('detalle')  # guarda detalles de la orden
        order = Order.objects.create(**validated_data)  # crea la orden

        for order_detail in details_data:
            # crea detalle de orden
            OrderDetail.objects.create(**order_detail, order=order)
            try:
                decrease_stock(order_detail)
            except Exception as e:
                return {
                    'error': str(e)
                }
        return order

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)

        details_data = validated_data.pop('detalle')
        detalle_dict = dict((i.id, i) for i in instance.detalle.all())
        for detalle in details_data:
            if 'id' in detalle:  # corrobora si hay id en lo que recibo desde el put.
                detalle_item = detalle_dict.pop((detalle['id']))
                detalle.pop('id')
                # MODIFICAMOS STOCK SEGUN CANTIDAD PRODUCTO QUE LLEGA POR EL PUT
                # si el producto es igual pero la cantidad diferente lo va a restar o sumar segun corresponda
                if detalle['product'] == detalle_item.product and detalle['quantity'] < detalle_item.quantity:
                    stock_a_modificar = detalle_item.quantity - detalle['quantity']
                    update_stock_sumar_diferencia(detalle_item,stock_a_modificar)
                elif detalle['product'] == detalle_item.product and detalle['quantity'] > detalle_item.quantity:
                    stock_a_modificar = detalle['quantity'] - detalle_item.quantity
                    update_stock_restar_diferencia(detalle_item, stock_a_modificar)
                for key in detalle.keys():
                    setattr(detalle_item, key, detalle[key])
                detalle_item.save()
            # si el prodcuto no tiene id en lo que me llega en el put quiere decir que es nuevo detalle
            # no estoy modificando un detalle, por ende se crea ese detalle y ademas se modifica el stock del prodcuto
            else:
                OrderDetail.objects.create(order=instance, **detalle)
                decrease_stock(detalle)
        if len(detalle_dict) > 0:  # corrobora si en el dict de instancias quedo alguna.
            for detalle in detalle_dict.values():
                # si eliminamos un detalle, se modifica el stock del producto tmb.
                add_stock(detalle)
                detalle.delete()

        return instance


class TotalOrderSerializer(serializers.Serializer):
    orden = serializers.IntegerField()
    total_cantidad_orden = serializers.IntegerField()
    monto_total = serializers.FloatField()
