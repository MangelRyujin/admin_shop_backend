from rest_framework import serializers
from apps.products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'likes', 'total_sales', 'is_deleted')

    def validate_image_list(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("image_list debe ser una lista")
        
        # Validar cada URL en la lista
        for image_url in value:
            if not isinstance(image_url, str):
                raise serializers.ValidationError("Cada imagen debe ser una URL string")
            
            # Validaciones básicas de URL (opcional)
            if not image_url.startswith(('http://', 'https://', '/media/', '/static/')):
                raise serializers.ValidationError(
                    f"URL de imagen no válida: {image_url}. Debe comenzar con http://, https://, /media/ o /static/"
                )
        
        # Limitar máximo de imágenes
        if len(value) > 10:
            raise serializers.ValidationError("Máximo 10 imágenes permitidas")
        
        return value

class ProductListSerializer(serializers.ModelSerializer):
    """Serializer optimizado para listados (menos campos)"""
    
    class Meta:
        model = Product
        fields = ('id', 'code', 'name', 'brand', 'stars', 'is_active')