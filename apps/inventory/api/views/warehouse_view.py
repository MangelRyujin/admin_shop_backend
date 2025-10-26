from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from apps.inventory.models import Warehouse
from apps.inventory.api.serializers.warehouse_serializer import WarehouseSerializer
from utils.pagination.pagination import Pagination 

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['store']
    search_fields = ['name', 'address', 'store__name']
    pagination_class = Pagination
    
    def get_queryset(self):
        queryset = Warehouse.objects.select_related('store')
        return queryset