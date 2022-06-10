"""ClickOH_Challenge URL Configuration
"""
from sys import path
path.append("../../")
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.api.views import ProductViewSet
from order.api.views import OrderViewSet
router = DefaultRouter()
router.register("products", ProductViewSet, basename='product')
router.register("orders", OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('', include(router.urls))
]
