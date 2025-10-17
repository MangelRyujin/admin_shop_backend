from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F, Value, Q
from django.db.models.functions import Coalesce
from django.db.models import Count
from rest_framework.response import Response
from apps.inventory.models import Stock
from apps.inventory.api.serializers.stock_serializer import StockSerializer, StockCreateSerializer, StockDetailSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['warehouse', 'product', 'is_active']
    search_fields = ['code', 'product__name', 'product__code']
    ordering_fields = ['cant', 'unit_price', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return StockCreateSerializer
        elif self.action == 'retrieve':
            return StockDetailSerializer
        return StockSerializer

    def get_queryset(self):
        return Stock.objects.select_related(
            'product', 'warehouse', 'warehouse__store'
        ).filter(is_active=True)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {
                    'error': 'Error al crear el stock',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=False, methods=['get'])
    def inventory_summary(self, request):
        try:
            summary = Stock.objects.filter(is_active=True).aggregate(
                total_products=Count('product', distinct=True),
                total_warehouses=Count('warehouse', distinct=True),
                total_quantity=Coalesce(Sum('cant'), Value(0)),
                total_value=Coalesce(Sum(F('cant') * F('unit_price')), Value(0))
            )
            return Response(summary)
        except Exception as e:
            return Response(
                {
                    'error': 'Error al generar el resumen de inventario',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        try:
            stock = self.get_object()
            adjustment = request.data.get('adjustment', 0)
            
            adjustment = int(adjustment)
            new_quantity = stock.cant + adjustment
            
            if new_quantity < 0:
                return Response(
                    {'error': 'La cantidad no puede ser negativa'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            stock.cant = new_quantity
            stock.save()
            
            return Response({
                'message': 'Stock ajustado correctamente',
                'new_quantity': stock.cant
            })
            
        except ValueError:
            return Response(
                {'error': 'El ajuste debe ser un número entero'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'error': 'Error al ajustar el stock',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def movements(self, request, pk=None):
        """
        Obtener movimientos de este stock específico
        """
        try:
            stock = self.get_object()
            from apps.inventory.models import StockMovement
            movements = StockMovement.objects.filter(
                Q(stock_one=stock) | Q(stock_two=stock)
            ).order_by('-created_date')
            
            from apps.inventory.api.serializers.stock_movement_serializer import StockMovementSerializer
            page = self.paginate_queryset(movements)
            if page is not None:
                serializer = StockMovementSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = StockMovementSerializer(movements, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener movimientos del stock',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )