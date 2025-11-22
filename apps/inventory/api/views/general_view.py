from rest_framework.views import APIView
from rest_framework.response import Response
from apps.inventory.models import Store, Warehouse, Stock
from apps.inventory.api.serializers.general_serializer import StoreSerializer, WarehouseSerializer, StockSerializer, ProductSerializer
from apps.products.models import Product


class WarehouseAndProductsListAPIView(APIView):
    
    def get(self, request):
        warehouses = Warehouse.objects.all().only("id", "name")
        products = Product.objects.all().only("id", "name")
        warehouses_serializer = WarehouseSerializer(warehouses, many=True)
        products_serializer = ProductSerializer(products, many=True)
        return Response({"products": products_serializer.data, "warehouses": warehouses_serializer.data, })

class StoreListAPIView(APIView):
    def get(self, request):
        stores = Store.objects.all().only("id", "name")
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)


class WarehouseListAPIView(APIView):
    def get(self, request):
        warehouses = Warehouse.objects.all().only("id", "name")
        serializer = WarehouseSerializer(warehouses, many=True)
        return Response(serializer.data)


class StockListAPIView(APIView):
    def get(self, request):
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)