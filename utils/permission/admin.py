from rest_framework.permissions import BasePermission

class IsAdminGroup(BasePermission):
    """
    Permiso personalizado que verifica si el usuario pertenece al grupo 'admin'
    """
    def has_permission(self, request, view):
        # Verifica que el usuario esté autenticado y pertenezca al grupo 'admin'
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.groups.filter(name='admin').exists()
        )
        
class HasPermission(BasePermission):
    def has_permission(self, request, view, permission_list):
        # Verifica que el usuario esté autenticado y pertenezca al grupo 'admin'
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.groups.filter(name__in=["admin", "seller"]).exists()
        )