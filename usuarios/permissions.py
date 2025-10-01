from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Permiso personalizado para verificar que el usuario es SUPER_ADMIN.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'perfil') and 
            request.user.perfil.rol == 'SUPER_ADMIN'
        )


class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Permiso para ADMIN o SUPER_ADMIN.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'perfil') and 
            request.user.perfil.rol in ['ADMIN', 'SUPER_ADMIN']
        )
