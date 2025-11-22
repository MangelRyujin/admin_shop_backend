from rest_framework import serializers
from apps.inventory.models import Store, Warehouse, Stock
from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name']


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name']


class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Stock
        fields = ['id', 'code', 'product','product_name']
        
    def get_product_name(self, obj):
        if obj.product:
            return obj.product.name
        return ""