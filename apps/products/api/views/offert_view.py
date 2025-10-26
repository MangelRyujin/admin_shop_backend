from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from apps.products.models import Offert
from apps.products.api.serializers.offert_serializer import (
    OffertSerializer, 
    OffertCreateSerializer, 
    OffertDetailSerializer,
    ActiveOffertSerializer
)
from utils.pagination.pagination import Pagination
from utils.permission.admin import IsAdminGroup

class OffertViewSet(viewsets.ModelViewSet):
    queryset = Offert.objects.all()
    permission_classes = [IsAuthenticated, IsAdminGroup]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'product']
    search_fields = ['name', 'description', 'product__name']
    ordering_fields = ['init_date', 'end_date', 'name']
    ordering = ['-init_date']
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action == 'create':
            return OffertCreateSerializer
        elif self.action == 'retrieve':
            return OffertDetailSerializer
        elif self.action == 'active_offerts':
            return ActiveOffertSerializer
        return OffertSerializer

    def get_queryset(self):
        return Offert.objects.select_related('product')

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                offert = serializer.save()
                response_serializer = OffertSerializer(offert)
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
                    'error': 'Error al crear la oferta',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            
            if serializer.is_valid():
                offert = serializer.save()
                response_serializer = OffertSerializer(offert)
                return Response(response_serializer.data)
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
                    'error': 'Error al actualizar la oferta',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def active_offerts(self, request):
        """
        Obtener ofertas activas (público) ;)
        """
        try:
            current_date = timezone.now().date()
            active_offerts = Offert.objects.filter(
                is_active=True,
                init_date__lte=current_date,
                end_date__gte=current_date
            ).select_related('product')
            
            page = self.paginate_queryset(active_offerts)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(active_offerts, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener ofertas activas',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def expired_offerts(self, request):
        try:
            current_date = timezone.now().date()
            expired_offerts = Offert.objects.filter(
                end_date__lt=current_date
            )
            
            serializer = OffertSerializer(expired_offerts, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener ofertas expiradas',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None): # Activar/desactivar ofertas chama
        try:
            offert = self.get_object()
            offert.is_active = not offert.is_active
            offert.save()
            
            message = "Oferta activada" if offert.is_active else "Oferta desactivada"
            return Response({
                'message': message,
                'is_active': offert.is_active
            })
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al cambiar estado de la oferta',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def upcoming_offerts(self, request):
        """
        Obtener ofertas próximas a iniciar --> Esto puede ser util luego ;)
        """
        try:
            current_date = timezone.now().date()
            upcoming_offerts = Offert.objects.filter(
                is_active=True,
                init_date__gt=current_date
            ).order_by('init_date')
            
            serializer = OffertSerializer(upcoming_offerts, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Error al obtener ofertas próximas',
                    'message': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )