from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from apps.accounts.api.serializers.user_serializer import UserSerializer
from apps.accounts.models import User
from utils.permission.admin import IsAdminGroup

class UserPagination(PageNumberPagination):
    """
    Configuración personalizada de paginación
    """
    page_size = 20  # Número de usuarios por página
    page_size_query_param = 'page_size'  # Permite al cliente especificar el tamaño de página
    max_page_size = 100  # Límite máximo de usuarios por página

class UserListView(generics.ListAPIView):
    """
    View para listar todos los usuarios
    Requiere autenticación y rol de administrador
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminGroup]
    pagination_class = UserPagination

    def get_queryset(self):
        """
        Personaliza el queryset con ordenación por email
        """
        queryset = User.objects.all()
        
        # Filtrar solo usuarios activos (opcional, descomenta si lo necesitas)
        # queryset = queryset.filter(is_active=True)
        
        # Ordenar por email
        queryset = queryset.order_by('id')
        
        return queryset