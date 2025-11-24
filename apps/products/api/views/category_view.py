from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

from apps.products.models import Category, SubCategory, Product
from apps.products.api.serializers.category_serializer import (
    CategorySerializer, CategoryDetailSerializer, CategoryCreateSerializer,
    SubCategorySerializer, SubCategoryCreateSerializer
)
from utils.pagination.pagination import Pagination
from utils.permission.admin import IsAdminGroup

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    pagination_class = Pagination
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def get_serializer_class(self):
        if self.action == 'create':
            return CategoryCreateSerializer
        elif self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        
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
                    
                       
                        serializer.errors
                    ,
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


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    pagination_class = Pagination
    permission_classes = [IsAuthenticated, IsAdminGroup]

    def get_serializer_class(self):
        if self.action == 'create':
            return SubCategoryCreateSerializer
        return SubCategorySerializer

    def get_queryset(self):
        return SubCategory.objects.select_related('category')