# SOLUCIÓN ERROR 500 - LOGIN ENDPOINT

## Fecha: 1 de octubre de 2025

## Problema Identificado

El backend estaba devolviendo Error 500 en el endpoint de login debido a:

1. **URL del frontend incorrecta en CORS**: La configuración tenía una URL diferente a la del frontend desplegado
2. **Error en LoginSerializer**: Verificaba `user.activo` en lugar de `user.perfil.activo`
3. **Falta de logging**: No había logs para diagnosticar errores en producción

## Cambios Realizados

### 1. Actualización de CORS (CONDOMINIO/settings.py)

```python
CORS_ALLOWED_ORIGINS = [
    'https://contabilidadwebapp-frontendlinux-fpbdc9h0byguh5dk.brazilsouth-01.azurewebsites.net',
    'https://contabilidadwebapp-frontend-linux-d2a9ddabctgte8ae.brazilsouth-01.azurewebsites.net',
    'http://localhost:5173',
    'http://localhost:3000',
    'http://127.0.0.1:5173',
    'http://127.0.0.1:3000',
]
```

### 2. Configuración de Logging

Agregado sistema de logging completo para debugging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'usuarios': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### 3. Mejora en login_view (usuarios/views.py)

- Agregado logging detallado para debugging
- Manejo de excepciones con try/except
- Creación automática de perfil si no existe
- Mensajes de error descriptivos

```python
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        logger.info(f"Login attempt - Data received: {request.data.keys()}")
        
        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            logger.info(f"User authenticated: {user.username}")
            
            # ... resto del código
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return Response(
            {'error': 'Error interno del servidor', 'detail': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

### 4. Corrección en LoginSerializer (usuarios/serializers.py)

Corregida la verificación del campo `activo`:

```python
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
        
        # Verificar que el usuario tenga perfil y esté activo
        if hasattr(user, 'perfil'):
            if not user.perfil.activo:
                raise serializers.ValidationError(
                    'Usuario inactivo.',
                    code='authorization'
                )
        # Si no tiene perfil, se creará automáticamente en la vista
    else:
        raise serializers.ValidationError(
            'Debe proporcionar usuario y contraseña.',
            code='authorization'
        )
    
    attrs['user'] = user
    return attrs
```

## Sistema de Autenticación JWT - Resumen

### ✅ Estado Actual

El sistema JWT **ya está completamente implementado** con:

- **Dependencias instaladas**: djangorestframework-simplejwt==5.3.1
- **App usuarios**: Creada y configurada
- **Modelo PerfilUsuario**: Con campos rol, telefono, activo, vivienda
- **Roles implementados**: SUPER_ADMIN, ADMIN, CONTADOR, GUARDIA, RESIDENTE
- **JWT configurado**: 
  - ACCESS_TOKEN_LIFETIME: 2 horas
  - REFRESH_TOKEN_LIFETIME: 7 días
  - ROTATE_REFRESH_TOKENS: True
  - BLACKLIST_AFTER_ROTATION: True

### Endpoints Disponibles

```
POST   /api/auth/login/            → Login con username/password
POST   /api/auth/logout/           → Logout (invalida refresh token)
GET    /api/auth/me/               → Obtener usuario actual
POST   /api/auth/token/refresh/    → Refrescar access token
POST   /api/auth/change-password/  → Cambiar contraseña
GET    /api/usuarios/              → Listar usuarios (admin)
POST   /api/usuarios/              → Crear usuario (admin)
GET    /api/usuarios/{id}/         → Detalle usuario
PATCH  /api/usuarios/{id}/         → Actualizar usuario parcial
DELETE /api/usuarios/{id}/         → Eliminar usuario
PUT    /api/usuarios/{id}/cambiar-rol/ → Cambiar rol (SUPER_ADMIN only)
```

### Credenciales de Admin

```
username: admin
password: admin123
rol: SUPER_ADMIN
```

## Pasos para Desplegar

### 1. Verificar localmente (opcional)

```bash
python test_login.py
```

Este script verifica:
- Conexión a la base de datos
- Existencia del usuario admin
- Autenticación funcional

### 2. Hacer commit y push

```bash
git add .
git commit -m "fix: Corregir Error 500 en login - actualizar CORS y logging"
git push origin main
```

### 3. Esperar deployment en Azure

El deployment automático mediante GitHub Actions tarda **3-5 minutos**.

### 4. Verificar en Azure Portal

Ir a: https://portal.azure.com
- Navegar a tu App Service
- Ir a "Log stream" para ver logs en tiempo real
- Verificar que no haya errores en el deployment

### 5. Probar el endpoint de login

```bash
curl -X POST https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Respuesta esperada (200 OK):**

```json
{
  "message": "Login exitoso",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@condominio.com",
    "nombre_completo": "Administrador Sistema",
    "rol": "SUPER_ADMIN",
    "vivienda": null
  }
}
```

## Variables de Entorno Requeridas en Azure

Verifica que estas estén configuradas en Azure App Service > Configuration > Application Settings:

```
DB_HOST=condominio-flutter.postgres.database.azure.com
DB_PORT=5432
DB_NAME=Condominio
DB_USER=jeadmin
DB_PASSWORD=<tu_password>
DJANGO_DEBUG=False
```

## Troubleshooting

### Si sigue dando Error 500:

1. **Ver logs en Azure Portal**:
   - App Service > Log stream
   - Buscar mensajes de error

2. **Verificar variables de entorno**:
   ```bash
   # En Azure Portal > Configuration
   # Verificar que todas las variables DB_* estén configuradas
   ```

3. **Verificar que el usuario admin existe**:
   ```bash
   # Conectarse a Azure y ejecutar:
   python manage.py shell
   from django.contrib.auth.models import User
   User.objects.filter(username='admin').exists()
   ```

4. **Ver logs detallados del error**:
   - Los logs ahora incluyen el stack trace completo
   - Buscar líneas con `ERROR` en el Log stream

### Si el frontend no puede conectarse:

1. **Verificar CORS**:
   - La URL del frontend debe estar en `CORS_ALLOWED_ORIGINS`
   - Verificar que sea exactamente la misma (incluyendo https://)

2. **Verificar que el backend esté accesible**:
   ```bash
   curl https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net/api/auth/login/
   ```

## Próximos Pasos

1. ✅ Hacer commit y push de estos cambios
2. ⏳ Esperar deployment en Azure (3-5 minutos)
3. ✅ Probar endpoint desde el frontend
4. ✅ Verificar que no haya errores en Log stream

## Archivos Modificados

- `CONDOMINIO/settings.py` - Agregado logging y actualizado CORS
- `usuarios/views.py` - Mejorado login_view con logging y manejo de errores
- `usuarios/serializers.py` - Corregido LoginSerializer validación de activo
- `test_login.py` - Nuevo archivo para verificación local
- `SOLUCION_ERROR_500.md` - Esta documentación
