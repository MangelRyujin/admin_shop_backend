from rest_framework import serializers
from apps.inventory.models import Store, Warehouse


class StoreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Store
        fields = ("id", "name")
        
class WarehouseSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

