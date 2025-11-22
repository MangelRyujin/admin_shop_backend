from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.inventory.api.views.warehouse_view import WarehouseViewSet
from apps.inventory.api.views.store_view import StoreViewSet
from apps.inventory.api.views.stock_view import StockViewSet
from apps.inventory.api.views.general_view import StoreListAPIView, WarehouseListAPIView, StockListAPIView, WarehouseAndProductsListAPIView

router = DefaultRouter()
router.register(r'stores', StoreViewSet, basename='stores')
router.register(r'warehouses', WarehouseViewSet, basename='warehouses')
router.register(r'stocks', StockViewSet, basename='stocks')

urlpatterns = [
    path('', include(router.urls)),
    path('stores-filter/', StoreListAPIView.as_view(), name="store-list-filter"),
    path('warehouses-filter/', WarehouseListAPIView.as_view(), name="warehouse-list-filter"),
    path('warehouses-and-products-filter/', WarehouseAndProductsListAPIView.as_view(), name="warehouse-and-products-list-filter"),
    path('stocks-filter/', StockListAPIView.as_view(), name="stock-list-filter"),
]
