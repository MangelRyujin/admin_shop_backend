from rest_framework import serializers
from apps.products.models import Category, SubCategory, Product

class SubCategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    full_path = serializers.SerializerMethodField()
    
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'is_active', 'products_count', 'full_path', 'created_at']
        read_only_fields = ['products_count', 'full_path']

    def get_products_count(self, obj):
        """Obtener cantidad de productos en la subcategoría"""
        return obj.products_count

    def get_full_path(self, obj):
        """Obtener ruta completa: Categoría → Subcategoría"""
        return f"{obj.category.name} → {obj.name}"

class SubCategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para creación de subcategorías
    """
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'description']

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
    """
    Serializer básico para categorías - CON IMAGEN
    """
    subcategories_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'image_url', 'is_active', 
                 'subcategories_count', 'products_count', 'created_at']
        read_only_fields = ['subcategories_count', 'products_count', 'image_url']

    def get_subcategories_count(self, obj):
        return obj.subcategories_count

    def get_products_count(self, obj):
        return obj.products_count

    def get_image_url(self, obj):
        """URL completa de la imagen"""
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None

from django.db import models
class CategoryDetailSerializer(CategorySerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    active_products_count = serializers.SerializerMethodField()
    
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['subcategories', 'active_products_count']
        
    def get_active_products_count(self, obj):
        """Productos activos en categoría y sus subcategorías"""
        return Product.objects.filter(
            models.Q(category=obj) | models.Q(subcategory__category=obj),
            is_active=True,
            is_deleted=False
        ).distinct().count()

import requests
from django.core.files.base import ContentFile
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description', 'image']
    
    def validate_name(self, value):
        """Validar nombre único"""
        if len(value.strip()) < 2:
            raise serializers.ValidationError("El nombre debe tener al menos 2 caracteres")
        return value

class CategoryWithProductsSerializer(CategorySerializer):
    featured_products = serializers.SerializerMethodField()
    
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['featured_products']

    def get_featured_products(self, obj):
        """Obtener productos destacados de la categoría"""
        from apps.products.api.serializers.product_serializer import ProductListSerializer
        
        featured_products = Product.objects.filter(
            models.Q(category=obj) | models.Q(subcategory__category=obj),
            is_active=True,
            is_deleted=False
        ).order_by('-stars', '-total_sales')[:6]  # Top 6 productos
        
        return ProductListSerializer(featured_products, many=True).data