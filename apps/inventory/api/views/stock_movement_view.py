from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Sum
from datetime import datetime, timedelta

from apps.inventory.models import StockMovement
from apps.inventory.api.serializers.stock_movement_serializer import (
    StockMovementSerializer, 
    StockMovementCreateSerializer
)
from utils.permission.admin import IsAdminGroup

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated, IsAdminGroup]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action_operation', 'action_type', 'user', 'stock_one', 'stock_two']
    search_fields = ['motive', 'description', 'stock_one__product__name', 'stock_one__product__code']
    ordering_fields = ['created_at', 'cant']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return StockMovementCreateSerializer
        return StockMovementSerializer

    def get_queryset(self):
        return StockMovement.objects.select_related(
            'stock_one', 'stock_one__product', 'stock_one__warehouse', 'stock_one__warehouse__store',
            'stock_two', 'stock_two__product', 'stock_two__warehouse', 'stock_two__warehouse__store',
            'user'
        )

    def create(self, request, *args, **kwargs):
        try:
            # Usar el serializer completo para creación con validaciones
            serializer = StockMovementSerializer(
                data=request.data,
                context={'request': request}
            )
            
            if serializer.is_valid():
                movement = serializer.save()
                response_serializer = StockMovementSerializer(movement)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {
                        'error': 'Error de validación en los datos',
                        'details': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {
                    'error': 'Error interno del servidor al crear el movimiento',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            
            if start_date:
                queryset = queryset.filter(created_at__gte=start_date)
            if end_date:
                queryset = queryset.filter(created_at__lte=end_date)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener la lista de movimientos',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        try:
            # Parámetros para el período
            days = int(request.query_params.get('days', 30))
            start_date = datetime.now() - timedelta(days=days)
            
            summary = StockMovement.objects.filter(
                created_at__gte=start_date
            ).aggregate(
                total_movements=Count('id'),
                total_entries=Count('id', filter=Q(action_operation='2')),
                total_exits=Count('id', filter=Q(action_operation='1')),
                total_quantity_moved=Sum('cant')
            )
            
            # Detalle por tipo de movimiento
            by_type = StockMovement.objects.filter(
                created_at__gte=start_date
            ).values('action_type').annotate(
                count=Count('id'),
                total_quantity=Sum('cant')
            )
            
            return Response({
                'period': f'Últimos {days} días',
                'summary': summary,
                'by_type': list(by_type)
            })
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al generar el resumen de movimientos',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def by_stock(self, request):
        """
        Obtener movimientos de un stock específico
        """
        try:
            stock_id = request.query_params.get('stock_id')
            if not stock_id:
                return Response(
                    {'error': 'El parámetro stock_id es requerido'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            movements = StockMovement.objects.filter(
                Q(stock_one_id=stock_id) | Q(stock_two_id=stock_id)
            ).order_by('-created_at')
            
            page = self.paginate_queryset(movements)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(movements, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener movimientos del stock',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )