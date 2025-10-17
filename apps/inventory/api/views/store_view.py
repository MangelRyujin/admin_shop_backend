from rest_framework import viewsets, filters
from apps.inventory.models import Store
from apps.inventory.api.serializers.store_serializer import StoreSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address']