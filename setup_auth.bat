@echo off
REM ============================================================================
REM Script automatizado para implementar autenticacion en el backend Django
REM ============================================================================

echo.
echo ========================================================================
echo   IMPLEMENTACION DE AUTENTICACION - BACKEND DJANGO
echo ========================================================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "manage.py" (
    echo ERROR: No se encuentra manage.py
    echo Por favor ejecuta este script desde: c:\Users\eduardo\Downloads\CondominioULT\CONDOMINIO\backend
    pause
    exit /b 1
)

echo [1/10] Activando entorno virtual...
cd ..
call venv\Scripts\activate
cd backend
echo OK - Entorno virtual activado
echo.

echo [2/10] Instalando dependencias...
pip install djangorestframework-simplejwt django-cors-headers --quiet
echo OK - Dependencias instaladas
echo.

echo [3/10] Creando app usuarios...
python manage.py startapp usuarios
echo OK - App usuarios creada
echo.

echo [4/10] Actualizando requirements.txt...
pip freeze > requirements.txt
echo OK - requirements.txt actualizado
echo.

echo.
echo ========================================================================
echo   PAUSA: Ahora necesitas EDITAR MANUALMENTE los archivos
echo ========================================================================
echo.
echo Sigue estos pasos en orden:
echo.
echo 1. Abre VS Code en la carpeta backend
echo.
echo 2. Edita CONDOMINIO/settings.py:
echo    - Agrega 'rest_framework_simplejwt' a INSTALLED_APPS
echo    - Agrega 'usuarios' a INSTALLED_APPS
echo    - Agrega la configuracion REST_FRAMEWORK al final
echo    - Agrega la configuracion SIMPLE_JWT al final
echo    - Agrega AUTH_USER_MODEL = 'usuarios.Usuario'
echo    - Cambia CORS_ALLOW_ALL_ORIGINS = False
echo    - Agrega CORS_ALLOW_CREDENTIALS = True
echo.
echo 3. Crea/edita estos archivos segun la guia:
echo    - usuarios/models.py (Modelo Usuario)
echo    - usuarios/serializers.py (CREAR - Serializers)
echo    - usuarios/views.py (Views de autenticacion)
echo    - usuarios/urls.py (CREAR - URLs)
echo    - CONDOMINIO/api_urls.py (agregar include usuarios.urls)
echo.
echo 4. Cuando termines, presiona cualquier tecla para continuar...
pause

echo.
echo [5/10] Creando migraciones...
python manage.py makemigrations usuarios
if %errorlevel% neq 0 (
    echo ERROR: Hubo un problema al crear las migraciones
    echo Revisa que hayas editado correctamente usuarios/models.py
    pause
    exit /b 1
)
echo OK - Migraciones creadas
echo.

echo [6/10] Aplicando migraciones...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Hubo un problema al aplicar las migraciones
    pause
    exit /b 1
)
echo OK - Migraciones aplicadas
echo.

echo.
echo ========================================================================
echo   CREAR SUPERUSUARIO
echo ========================================================================
echo.
echo Ahora vamos a crear el usuario administrador.
echo.
python manage.py createsuperuser
echo.

echo [7/10] Configurando rol del superusuario...
python manage.py shell -c "from usuarios.models import Usuario; u = Usuario.objects.first(); u.rol = 'SUPER_ADMIN'; u.first_name = 'Admin'; u.save(); print(f'Usuario {u.username} configurado como {u.get_rol_display()}')"
echo OK - Superusuario configurado
echo.

echo [8/10] Iniciando servidor de prueba...
echo.
echo El servidor se iniciara en http://localhost:8000
echo.
echo PRUEBA ESTO EN OTRO TERMINAL:
echo.
echo curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"tu_password\"}"
echo.
echo Presiona Ctrl+C para detener el servidor cuando termines de probar
echo.
python manage.py runserver

echo.
echo ========================================================================
echo   COMPLETADO!
echo ========================================================================
echo.
echo Ahora puedes:
echo 1. Hacer commit y push de los cambios
echo 2. Deployar a Azure
echo 3. Implementar el frontend con login
echo.
pause
