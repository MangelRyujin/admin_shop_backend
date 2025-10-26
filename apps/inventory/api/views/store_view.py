from rest_framework import viewsets, filters, pagination
from apps.inventory.models import Store
from apps.inventory.api.serializers.store_serializer import StoreSerializer
from utils.pagination.pagination import Pagination

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']
    pagination_class = Pagination
