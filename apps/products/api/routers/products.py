from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.products.api.views.product_view import ProductViewSet 
from apps.products.api.views.offert_view import OffertViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products'),
router.register(r'offerts', OffertViewSet, basename='offerts')

urlpatterns = [
    path('', include(router.urls)),
]