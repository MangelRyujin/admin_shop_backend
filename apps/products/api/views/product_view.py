from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.products.models import Product
from apps.products.api.serializers.product_serializer import ProductSerializer, ProductListSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'brand']
    search_fields = ['code', 'name', 'brand']
    ordering_fields = ['name', 'created_at', 'stars', 'total_sales']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        product = self.get_object()
        product.is_active = not product.is_active
        product.save()
        return Response({'status': 'active toggled', 'is_active': product.is_active})

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        stats = {
            'total_products': Product.objects.filter(is_deleted=False).count(),
            'active_products': Product.objects.filter(is_active=True, is_deleted=False).count(),
            'total_brands': Product.objects.filter(is_deleted=False).values('brand').distinct().count(),
        }
        return Response(stats)