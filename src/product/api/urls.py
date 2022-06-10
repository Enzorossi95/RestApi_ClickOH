from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..api.views import ProductViewSet
"""
Vacio, decidi que lo maneje el router en el archivo principal.

Cabe aclarar que se podria manejar las rutas interas aqui , en este caso de la app order. Pero al ser un proyecto pequeño
lo decidi manejar en el archivo general.

Si, las buenas practicas dicen que se deberia manejar aqui las rutas interas de esta app.

"""

urlpatterns = [

]
