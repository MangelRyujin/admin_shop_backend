from rest_framework import serializers
from apps.inventory.models import Stock

class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.code', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    store_name = serializers.CharField(source='warehouse.store.name', read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class StockCreateSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Stock
        fields = ('product', 'warehouse', 'cant', 'unit_price', 'code', 'expire_date', 'threshold')

    def validate(self, data):
        # Validar que no exista stock duplicado para el mismo producto/warehouse
        if data['product'] and data['warehouse']:
            if Stock.objects.filter(
                product=data['product'], 
                warehouse=data['warehouse']
            ).exists():
                raise serializers.ValidationError(
                    "Ya existe stock para este producto en el almacén seleccionado."
                )
        return data

class StockDetailSerializer(StockSerializer):
    product_details = serializers.SerializerMethodField()

    def get_product_details(self, obj):
        from apps.products.api.serializers.product_serializer import ProductListSerializer
        return ProductListSerializer(obj.product).data

    class Meta(StockSerializer.Meta):
        fields = [  # Lista explícita de campos
            'id', 'product', 'product_name', 'product_code', 'warehouse', 
            'warehouse_name', 'store_name', 'cant', 'unit_price', 'is_active', 
            'created_at', 'updated_at', 'product_details'
        ]
