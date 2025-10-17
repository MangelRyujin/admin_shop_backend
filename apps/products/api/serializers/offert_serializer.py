from rest_framework import serializers
from django.utils import timezone
from apps.products.models import Offert
from apps.products.api.serializers.product_serializer import ProductListSerializer

class OffertSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_code = serializers.CharField(source='product.code', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Offert
        fields = '__all__'

    def validate(self, data):
        init_date = data.get('init_date')
        end_date = data.get('end_date')
        
        # Validar que la fecha de inicio no sea en el pasado
        if init_date and init_date < timezone.now().date():
            raise serializers.ValidationError({
                'init_date': 'La fecha de inicio no puede ser en el pasado'
            })
        
        # Validar que la fecha de fin sea mayor a la de inicio
        if init_date and end_date and end_date <= init_date:
            raise serializers.ValidationError({
                'end_date': 'La fecha de fin debe ser posterior a la fecha de inicio'
            })
        
        # Validar que el producto esté activo
        product = data.get('product')
        if product and (not product.is_active or product.is_deleted):
            raise serializers.ValidationError({
                'product': 'El producto debe estar activo'
            })
        
        return data

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError('El nombre debe tener al menos 3 caracteres')
        return value

class OffertCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offert
        fields = ['product', 'name', 'description', 'init_date', 'end_date']

class OffertDetailSerializer(OffertSerializer):
    product_details = ProductListSerializer(source='product', read_only=True)
    
    class Meta(OffertSerializer.Meta):
        fields = [
            'id', 'name', 'description', 'init_date', 'end_date', 
            'product_name', 'product_code', 'is_active', 'product_details'
        ]

class ActiveOffertSerializer(serializers.ModelSerializer):
    """
    Serializer para ofertas activas (uso público)
    """
    product_details = ProductListSerializer(source='product', read_only=True)
    days_remaining = serializers.SerializerMethodField()
    
    class Meta:
        model = Offert
        fields = ['id', 'name', 'description', 'init_date', 'end_date', 'product_details', 'days_remaining']
    
    def get_days_remaining(self, obj):
        if obj.end_date:
            remaining = (obj.end_date - timezone.now().date()).days
            return max(0, remaining)
        return None