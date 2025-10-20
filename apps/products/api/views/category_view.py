from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from apps.products.models import Category, SubCategory, Product
from apps.products.api.serializers.category_serializer import (
    CategorySerializer, CategoryDetailSerializer, CategoryCreateSerializer,
    CategoryWithProductsSerializer, SubCategorySerializer, SubCategoryCreateSerializer
)
from utils.permission.admin import IsAdminGroup

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at', 'products_count']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'with_products', 'hierarchy']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminGroup]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryCreateSerializer
        elif self.action == 'retrieve':
            return CategoryDetailSerializer
        elif self.action == 'with_products':
            return CategoryWithProductsSerializer
        return CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(is_active=True)
        
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('subcategories')
        elif self.action == 'with_products':
            queryset = queryset.prefetch_related('subcategories')
            
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                category = serializer.save()
                response_serializer = CategorySerializer(category)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {
                        'error': 'Error de validación',
                        'details': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {
                    'error': 'Error al crear la categoría',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def with_products(self, request):
        """
        Obtener categorías con productos destacados
        Para páginas de catálogo público
        """
        try:
            categories = self.get_queryset()
            serializer = self.get_serializer(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener categorías con productos',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def hierarchy(self, request):
        """
        Obtener estructura jerárquica completa de categorías y subcategorías
        Para menús de navegación
        """
        try:
            categories = Category.objects.filter(is_active=True).prefetch_related(
                'subcategories'
            )
            
            hierarchy_data = []
            for category in categories:
                category_data = {
                    'id': category.id,
                    'name': category.name,
                    'image_url': category.image.url if category.image else None,
                    'subcategories': []
                }
                
                # Agregar subcategorías activas
                for subcategory in category.subcategories.filter(is_active=True):
                    category_data['subcategories'].append({
                        'id': subcategory.id,
                        'name': subcategory.name,
                        'products_count': subcategory.products_count
                    })
                
                hierarchy_data.append(category_data)
            
            return Response(hierarchy_data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener la jerarquía de categorías',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        Obtener TODOS los productos de una categoría (incluyendo subcategorías)
        """
        try:
            category = self.get_object()
            
            # Productos de la categoría principal Y de sus subcategorías
            products = Product.objects.filter(
                Q(category=category) | Q(subcategory__category=category),
                is_active=True,
                is_deleted=False
            ).distinct()
            
            from apps.products.api.serializers.product_serializer import ProductListSerializer
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = ProductListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener productos de la categoría',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.filter(is_active=True)
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAdminGroup]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return SubCategoryCreateSerializer
        return SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.select_related('category')

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        Obtener productos de una subcategoría específica
        """
        try:
            subcategory = self.get_object()
            products = subcategory.products.filter(is_active=True, is_deleted=False)
            
            from apps.products.api.serializers.product_serializer import ProductListSerializer
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = ProductListSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = ProductListSerializer(products, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener productos de la subcategoría',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Obtener subcategorías por categoría específica
        """
        try:
            category_id = request.query_params.get('category_id')
            if not category_id:
                return Response(
                    {'error': 'El parámetro category_id es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            subcategories = SubCategory.objects.filter(
                category_id=category_id, 
                is_active=True
            )
            serializer = self.get_serializer(subcategories, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener subcategorías por categoría',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )