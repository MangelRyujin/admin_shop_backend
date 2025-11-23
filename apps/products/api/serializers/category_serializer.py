from rest_framework import serializers
from apps.products.models import Category, SubCategory, Product
from django.db import models

class SubCategorySerializer(serializers.ModelSerializer):
    
    full_path = serializers.SerializerMethodField()
    
    class Meta:
        model = SubCategory
        fields = ['id', 'name',  'created_at', 'created_at']
        read_only_fields = ['products_count', 'full_path']

    def get_products_count(self, obj):
        """Obtener cantidad de productos en la subcategoría"""
        return obj.products_count

    def get_full_path(self, obj):
        """Obtener ruta completa: Categoría → Subcategoría"""
        return f"{obj.category.name} → {obj.name}"

class SubCategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ['category', 'name']

    def validate(self, data):
        """Validar que no exista subcategoría con mismo nombre en la misma categoría"""
        category = data.get('category')
        name = data.get('name')
        
        if SubCategory.objects.filter(category=category, name=name).exists():
            raise serializers.ValidationError({
                'name': 'Ya existe una subcategoría con este nombre en la misma categoría'
            })
        return data

class CategorySerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'image_url', 'created_at', 'updated_at']
        read_only_fields = ['image_url']

    def get_image_url(self, obj):
        """URL completa de la imagen"""
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None


class CategoryDetailSerializer(CategorySerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
   
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['subcategories']
        

class CategoryCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['name', 'image']
    
    def validate_name(self, value):
        """Validar nombre único"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        return value
