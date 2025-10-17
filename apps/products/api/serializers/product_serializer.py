from rest_framework import serializers
from apps.products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'likes', 'total_sales')

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer optimizado para listados (menos campos)"""
    
    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'brand', 'stars', 'is_active')