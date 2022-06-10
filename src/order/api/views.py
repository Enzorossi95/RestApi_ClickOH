#import paquetes de rest
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

#import paquetes locales
from .serializers import OrderSerializer, TotalOrderSerializer
from ..models import Order, OrderDetail
from ..utils import valor_actual_dolar_blue_venta, add_stock


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    # reescribimos el metodo para agregar el stock de lo que se elimina.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        details_data = instance.detalle.all()
        for order_detail in details_data:
            try:
                add_stock(order_detail)
            except Exception as e:
                return Response({
                    'Message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response({
                    'Message': 'Objeto eliminado'
                }, status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['get'])
    def total_order(self, request, pk=None):  # end_ponit para total de la orden
        orden = self.get_object()
        try:
            suma_total_cantidad = sum([i.quantity for i in orden.detalle.all()])
            monto_total = sum([j.product.price for j in orden.detalle.all()])
            data = {
                'orden': orden.number,
                'total_cantidad_orden': suma_total_cantidad,
                'monto_total': monto_total
            }
            serializer = TotalOrderSerializer(data)
            return Response({
                'Message': 'Success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'Message': 'Total orden',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def total_order_dolar_blue(self, request, pk=None):  # end_point para el total de la orden en dolar blue
        orden = self.get_object()
        try:
            dolar_blue = valor_actual_dolar_blue_venta()
            suma_total_cantidad = sum([i.quantity for i in orden.detalle.all()])
            monto_total = sum([j.product.price for j in orden.detalle.all()]) * dolar_blue
            data = {
                'orden': orden.number,
                'total_cantidad_orden': suma_total_cantidad,
                'monto_total': monto_total
            }
            serializer = TotalOrderSerializer(data)
            return Response({
                'Message': 'Success',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'Message': 'Total orden',
                'Error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
