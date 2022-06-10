from ..models import Product
from rest_framework import serializers

""""
Serializers, archivo corazon de la app Producto

"""


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class StockSerializer(serializers.Serializer):
    model = Product
    stock = serializers.IntegerField()
