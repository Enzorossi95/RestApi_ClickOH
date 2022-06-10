#import paquetes de rest
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
#import paquetes locales
from .serializers import ProductSerializer, StockSerializer
from ..models import Product

from rest_framework.authentication import TokenAuthentication


class ProductViewSet(viewsets.ModelViewSet):
    """
    Viewset para productos.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        producto = self.get_object()
        stock_serializer = StockSerializer(data=request.data)
        if stock_serializer.is_valid():
            producto.stock = stock_serializer.validated_data['stock']
            producto.save()
            return Response({
                'Message': 'Stock actualizado',
                'Stock_Actual': stock_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "res": f"Se produjo un error",
            'errors': stock_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
