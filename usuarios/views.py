from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.contrib.auth.models import User

from .models import PerfilUsuario
from .serializers import (
    UsuarioSerializer,
    UsuarioCreateSerializer,
    UsuarioUpdateSerializer,
    LoginSerializer,
    ChangePasswordSerializer
)
from .permissions import IsSuperAdmin, IsAdminOrSuperAdmin


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Vista de login que retorna tokens JWT."""
    serializer = LoginSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        nombre_completo = f"{user.first_name} {user.last_name}".strip() or user.username
        perfil = getattr(user, 'perfil', None)
        
        return Response({
            'message': 'Login exitoso',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'nombre_completo': nombre_completo,
                'rol': perfil.rol if perfil else 'RESIDENTE',
                'vivienda': perfil.vivienda_id if perfil else None,
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Vista de logout que invalida el refresh token."""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        logout(request)
        return Response({
            'message': 'Logout exitoso'
        }, status=status.HTTP_200_OK)
    except Exception:
        return Response({
            'error': 'Token inválido'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Obtiene la información del usuario autenticado."""
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """Cambia la contraseña del usuario autenticado."""
    serializer = ChangePasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Contraseña cambiada exitosamente'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para CRUD de usuarios (solo administradores)."""
    
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UsuarioUpdateSerializer
        return UsuarioSerializer
    
    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /api/usuarios/{id}/
        Actualización parcial del usuario (incluyendo campo activo).
        """
        usuario = self.get_object()
        serializer = UsuarioUpdateSerializer(usuario, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            # Retornar con el serializer completo
            response_serializer = UsuarioSerializer(usuario)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        PUT /api/usuarios/{id}/
        Actualización completa del usuario.
        """
        usuario = self.get_object()
        serializer = UsuarioUpdateSerializer(usuario, data=request.data, partial=False)
        
        if serializer.is_valid():
            serializer.save()
            # Retornar con el serializer completo
            response_serializer = UsuarioSerializer(usuario)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def publico(self, request):
        """Lista de usuarios público (sin autenticación)."""
        usuarios = self.get_queryset()
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], url_path='cambiar-rol', permission_classes=[IsAuthenticated, IsSuperAdmin])
    def cambiar_rol(self, request, pk=None):
        """
        PUT /api/usuarios/{id}/cambiar-rol/
        Cambia el rol de un usuario (solo SUPER_ADMIN).
        """
        usuario = self.get_object()
        nuevo_rol = request.data.get('rol')
        
        if not nuevo_rol:
            return Response(
                {'error': 'El campo "rol" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar que el rol existe
        roles_validos = [rol[0] for rol in PerfilUsuario.ROL_CHOICES]
        if nuevo_rol not in roles_validos:
            return Response(
                {
                    'error': 'Rol inválido',
                    'roles_validos': roles_validos
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # No permitir cambiar el rol de uno mismo
        if usuario.id == request.user.id:
            return Response(
                {'error': 'No puedes cambiar tu propio rol'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Actualizar rol
        perfil = usuario.perfil
        perfil.rol = nuevo_rol
        perfil.save()
        
        serializer = UsuarioSerializer(usuario)
        return Response({
            'message': f'Rol actualizado a {perfil.get_rol_display()}',
            'usuario': serializer.data
        })
