from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.inventory.api.views.warehouse_view import WarehouseViewSet
from apps.inventory.api.views.store_view import StoreViewSet
from apps.inventory.api.views.stock_view import StockViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename='stores')
router.register(r'warehouses', WarehouseViewSet, basename='warehouses')
router.register(r'stocks', StockViewSet, basename='stocks')

urlpatterns = [
    path('', include(router.urls)),
]