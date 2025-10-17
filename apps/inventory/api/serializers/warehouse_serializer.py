from rest_framework import serializers
from apps.inventory.models import Warehouse

class WarehouseSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

