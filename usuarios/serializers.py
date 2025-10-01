from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import PerfilUsuario


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    """Serializer para el perfil del usuario."""
    
    class Meta:
        model = PerfilUsuario
        fields = ['rol', 'telefono', 'vivienda', 'activo']


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer para mostrar información del usuario."""
    
    perfil = PerfilUsuarioSerializer(read_only=True)
    rol = serializers.CharField(source='perfil.rol', read_only=True)
    telefono = serializers.CharField(source='perfil.telefono', read_only=True)
    vivienda = serializers.IntegerField(source='perfil.vivienda_id', read_only=True)
    activo = serializers.BooleanField(source='perfil.activo', read_only=True)
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'nombre_completo',
            'rol',
            'telefono',
            'vivienda',
            'activo',
            'perfil',
        ]
        read_only_fields = ['id']
    
    def get_nombre_completo(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear nuevos usuarios."""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    rol = serializers.ChoiceField(choices=PerfilUsuario.ROL_CHOICES, default='RESIDENTE')
    telefono = serializers.CharField(required=False, allow_blank=True)
    vivienda = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'rol',
            'telefono',
            'vivienda',
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Las contraseñas no coinciden."
            })
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        # Extraer datos del perfil
        rol = validated_data.pop('rol', 'RESIDENTE')
        telefono = validated_data.pop('telefono', '')
        vivienda_id = validated_data.pop('vivienda', None)
        
        # Crear usuario
        usuario = User.objects.create(**validated_data)
        usuario.set_password(password)
        usuario.save()
        
        # Actualizar perfil
        perfil = usuario.perfil
        perfil.rol = rol
        perfil.telefono = telefono
        if vivienda_id:
            perfil.vivienda_id = vivienda_id
        perfil.save()
        
        return usuario


class LoginSerializer(serializers.Serializer):
    """Serializer para login."""
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Credenciales inválidas.',
                    code='authorization'
                )
            
            if not user.activo:
                raise serializers.ValidationError(
                    'Usuario inactivo.',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Debe proporcionar usuario y contraseña.',
                code='authorization'
            )
        
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para cambiar contraseña."""
    
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Las contraseñas no coinciden."
            })
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Contraseña actual incorrecta.')
        return value
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
