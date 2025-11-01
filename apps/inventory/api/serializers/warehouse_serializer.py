from rest_framework import serializers
from apps.inventory.models import Store, Warehouse


class WarehouseStoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store
        fields = ("id", "name")
        
class WarehouseSerializer(serializers.ModelSerializer):
    store_detail = WarehouseStoreSerializer(source="store", read_only=True)
    
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')