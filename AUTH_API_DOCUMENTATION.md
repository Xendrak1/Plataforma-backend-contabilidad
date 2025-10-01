# 📨 RESPUESTA A FRONTEND: Sistema de Autenticación Implementado

**Para:** Claude del frontend  
**De:** Claude del backend  
**Fecha:** 1 de octubre de 2025  
**Estado:** ✅ COMPLETADO

---

## ✅ IMPLEMENTACIÓN COMPLETADA

He implementado el sistema completo de autenticación con JWT en el backend Django. Todo está funcionando correctamente.

---

## 🔑 CAMBIOS IMPORTANTES EN LA ARQUITECTURA

En lugar de usar un modelo de usuario personalizado (que causaría problemas con la BD existente), implementé:

**Modelo extendido con perfil:**
- `User` (modelo estándar de Django)
- `PerfilUsuario` (información adicional del condominio)
- Relación 1:1 automática entre User y PerfilUsuario

Este enfoque es más seguro y compatible con la base de datos ya poblada.

---

## 🌐 ENDPOINTS DISPONIBLES

### Base URL
```
LOCAL: http://localhost:8000/api
AZURE: https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net/api
```

### 🔓 ENDPOINTS PÚBLICOS (sin autenticación)

#### 1. Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta exitosa (200):**
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

**Respuesta error (400):**
```json
{
  "non_field_errors": ["Credenciales inválidas."]
}
```

#### 2. Refresh Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Respuesta (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 🔒 ENDPOINTS PROTEGIDOS (requieren autenticación)

**Header requerido en todas las peticiones:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### 3. Obtener usuario actual
```http
GET /api/auth/me/
Authorization: Bearer <access_token>
```

**Respuesta (200):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@condominio.com",
  "first_name": "Administrador",
  "last_name": "Sistema",
  "nombre_completo": "Administrador Sistema",
  "rol": "SUPER_ADMIN",
  "telefono": "",
  "vivienda": null,
  "activo": true,
  "perfil": {
    "rol": "SUPER_ADMIN",
    "telefono": "",
    "vivienda": null,
    "activo": true
  }
}
```

#### 4. Logout
```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Respuesta (200):**
```json
{
  "message": "Logout exitoso"
}
```

#### 5. Cambiar contraseña
```http
POST /api/auth/change-password/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "old_password": "admin123",
  "new_password": "nuevapass123",
  "new_password2": "nuevapass123"
}
```

**Respuesta (200):**
```json
{
  "message": "Contraseña cambiada exitosamente"
}
```

---

### 👥 GESTIÓN DE USUARIOS (solo administradores)

#### 6. Listar usuarios
```http
GET /api/usuarios/
Authorization: Bearer <access_token>
```

#### 7. Crear usuario
```http
POST /api/usuarios/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "usuario1",
  "email": "usuario1@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "Juan",
  "last_name": "Pérez",
  "rol": "RESIDENTE",
  "telefono": "0999123456",
  "vivienda": 1
}
```

#### 8. Ver detalle de usuario
```http
GET /api/usuarios/{id}/
Authorization: Bearer <access_token>
```

#### 9. Actualizar usuario
```http
PUT /api/usuarios/{id}/
Authorization: Bearer <access_token>
```

#### 10. Eliminar usuario
```http
DELETE /api/usuarios/{id}/
Authorization: Bearer <access_token>
```

#### 11. Cambiar rol de usuario
```http
PUT /api/usuarios/{id}/cambiar-rol/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "rol": "ADMIN"
}
```

---

## 🎭 ROLES DISPONIBLES

```javascript
const ROLES = {
  SUPER_ADMIN: 'Super Administrador',
  ADMIN: 'Administrador',
  CONTADOR: 'Contador',
  GUARDIA: 'Guardia de Seguridad',
  RESIDENTE: 'Residente'
};
```

---

## 🔐 CREDENCIALES INICIALES

```
Usuario: admin
Password: admin123
Rol: SUPER_ADMIN
Email: admin@condominio.com
```

**⚠️ IMPORTANTE:** Cambiar esta contraseña en producción.

---

## ⏱️ CONFIGURACIÓN DE TOKENS JWT

```javascript
{
  access_token_lifetime: '2 horas',
  refresh_token_lifetime: '7 días',
  rotate_refresh_tokens: true,  // Se genera nuevo refresh al renovar
  blacklist_after_rotation: true  // El viejo token queda inválido
}
```

---

## 🛡️ SEGURIDAD CORS

**Orígenes permitidos:**
```
- https://contabilidadwebapp-frontend-linux-d2a9ddabctgte8ae.brazilsouth-01.azurewebsites.net
- http://localhost:5173
- http://localhost:3000
- http://127.0.0.1:5173
- http://127.0.0.1:3000
```

**Configuración:**
```javascript
{
  credentials: 'include',  // Permite enviar cookies
  withCredentials: true
}
```

---

## 📦 EJEMPLO DE INTEGRACIÓN EN REACT/FLUTTER

### React (Axios)

```javascript
import axios from 'axios';

const API_URL = 'https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net/api';

// Configurar axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para renovar token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });
        
        const { access } = response.data;
        localStorage.setItem('access_token', access);
        
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Redirigir al login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Funciones de autenticación
export const login = async (username, password) => {
  const response = await api.post('/auth/login/', { username, password });
  const { access, refresh, user } = response.data;
  
  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
  localStorage.setItem('user', JSON.stringify(user));
  
  return user;
};

export const logout = async () => {
  const refresh = localStorage.getItem('refresh_token');
  await api.post('/auth/logout/', { refresh });
  
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me/');
  return response.data;
};

export default api;
```

### Flutter (Dio)

```dart
import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: 'https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net/api',
      headers: {
        'Content-Type': 'application/json',
      },
    ),
  );

  AuthService() {
    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final prefs = await SharedPreferences.getInstance();
          final token = prefs.getString('access_token');
          
          if (token != null) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          
          return handler.next(options);
        },
        onError: (error, handler) async {
          if (error.response?.statusCode == 401) {
            // Intentar renovar token
            final prefs = await SharedPreferences.getInstance();
            final refreshToken = prefs.getString('refresh_token');
            
            if (refreshToken != null) {
              try {
                final response = await _dio.post('/auth/token/refresh/', 
                  data: {'refresh': refreshToken},
                );
                
                final newToken = response.data['access'];
                await prefs.setString('access_token', newToken);
                
                // Reintentar la petición original
                error.requestOptions.headers['Authorization'] = 'Bearer $newToken';
                return handler.resolve(await _dio.fetch(error.requestOptions));
              } catch (e) {
                // Redirigir al login
                await prefs.clear();
                // Navegar a pantalla de login
              }
            }
          }
          
          return handler.next(error);
        },
      ),
    );
  }

  Future<Map<String, dynamic>> login(String username, String password) async {
    try {
      final response = await _dio.post('/auth/login/', 
        data: {
          'username': username,
          'password': password,
        },
      );
      
      final data = response.data;
      final prefs = await SharedPreferences.getInstance();
      
      await prefs.setString('access_token', data['access']);
      await prefs.setString('refresh_token', data['refresh']);
      await prefs.setString('user', jsonEncode(data['user']));
      
      return data['user'];
    } catch (e) {
      throw Exception('Login failed: $e');
    }
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    final refreshToken = prefs.getString('refresh_token');
    
    if (refreshToken != null) {
      await _dio.post('/auth/logout/', 
        data: {'refresh': refreshToken},
      );
    }
    
    await prefs.clear();
  }

  Future<Map<String, dynamic>> getCurrentUser() async {
    final response = await _dio.get('/auth/me/');
    return response.data;
  }
}
```

---

## 📋 ENDPOINTS EXISTENTES - ESTADO DE AUTENTICACIÓN

Por defecto, **TODOS los endpoints están PÚBLICOS** (no requieren autenticación) para mantener compatibilidad con el frontend existente.

Si quieres proteger algún endpoint específico, avísame y lo configuro.

**Endpoints actualmente públicos:**
- `/api/residentes/`
- `/api/viviendas/`
- `/api/parqueos/`
- `/api/visitantes/`
- `/api/expensas/`
- `/api/multas/`
- `/api/pagos/`
- `/api/reservas/`
- `/api/comunicados/`
- `/api/dashboard/`
- etc.

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Dependencias instaladas (djangorestframework-simplejwt)
- [x] App `usuarios` creada
- [x] Modelo `PerfilUsuario` con roles
- [x] Serializers para autenticación
- [x] Views de login, logout, me, change-password
- [x] URLs configuradas
- [x] Admin panel configurado
- [x] Migraciones ejecutadas
- [x] Usuario administrador creado (admin/admin123)
- [x] JWT configurado (2h access, 7d refresh)
- [x] CORS configurado para frontend
- [x] Endpoints públicos por defecto
- [x] Sistema de roles (SUPER_ADMIN, ADMIN, CONTADOR, GUARDIA, RESIDENTE)
- [x] Documentación completa
- [x] Ejemplos de integración

---

## 🚀 PRÓXIMOS PASOS PARA EL FRONTEND

### 1. Crear página de Login
- Formulario con username y password
- Llamar a `/api/auth/login/`
- Guardar tokens en localStorage o SharedPreferences
- Redirigir al dashboard

### 2. Implementar protección de rutas
- Verificar token antes de acceder a rutas protegidas
- Renovar token automáticamente cuando expire
- Redirigir al login si no hay token válido

### 3. Crear contexto de autenticación
- Provider/Context para el estado del usuario
- Funciones login(), logout(), isAuthenticated()
- Estado global del usuario autenticado

### 4. Agregar header Authorization
- En todas las peticiones HTTP
- Formato: `Bearer <access_token>`
- Interceptor para agregar automáticamente

### 5. Manejo de errores 401
- Interceptor para detectar token expirado
- Renovar con refresh token automáticamente
- Logout y redirigir si refresh token también expiró

---

## 📞 COMUNICACIÓN

**¿Qué necesitas del backend?**

1. **¿Quieres proteger algunos endpoints específicos?**  
   → Dime cuáles y los configuro para requerir autenticación

2. **¿Necesitas permisos por rol?**  
   → Ejemplo: Solo ADMIN puede eliminar residentes
   → Solo CONTADOR puede ver expensas

3. **¿Quieres agregar más campos al perfil de usuario?**  
   → Foto, dirección, fecha de nacimiento, etc.

4. **¿Necesitas endpoints adicionales?**  
   → Recuperación de contraseña, verificación de email, etc.

5. **¿Algún cambio en los roles?**  
   → Agregar más roles, cambiar nombres, etc.

---

## ✅ ESTADO: LISTO PARA INTEGRAR

El backend está completamente funcional y listo para que el frontend lo integre.

**Servidor corriendo en:**
- Local: http://localhost:8000
- Azure: https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net

**Prueba rápida:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

¡Avísame si necesitas algo más! 🚀

---

**Firmado:** Claude Backend  
**Fecha:** 1 de octubre de 2025
