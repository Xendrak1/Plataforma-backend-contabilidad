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
    LoginSerializer,
    ChangePasswordSerializer
)


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
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UsuarioCreateSerializer
        return UsuarioSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def publico(self, request):
        """Lista de usuarios público (sin autenticación)."""
        usuarios = self.get_queryset()
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['put'], url_path='cambiar-rol')
    def cambiar_rol(self, request, pk=None):
        """Cambia el rol de un usuario."""
        usuario = self.get_object()
        nuevo_rol = request.data.get('rol')
        
        if nuevo_rol not in dict(PerfilUsuario.ROL_CHOICES):
            return Response(
                {'error': 'Rol inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        perfil = usuario.perfil
        perfil.rol = nuevo_rol
        perfil.save()
        
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)
