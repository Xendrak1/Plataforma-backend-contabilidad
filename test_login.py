"""
Script de prueba para verificar el endpoint de login localmente.
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONDOMINIO.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

def test_database_connection():
    """Verifica la conexión a la base de datos."""
    try:
        count = User.objects.count()
        print(f"✓ Conexión a BD exitosa. Usuarios en la base: {count}")
        return True
    except Exception as e:
        print(f"✗ Error de conexión a BD: {e}")
        return False

def test_admin_user():
    """Verifica que existe el usuario admin."""
    try:
        admin = User.objects.get(username='admin')
        print(f"✓ Usuario admin encontrado (ID: {admin.id})")
        
        # Verificar perfil
        if hasattr(admin, 'perfil'):
            perfil = admin.perfil
            print(f"  - Rol: {perfil.rol}")
            print(f"  - Activo: {perfil.activo}")
            print(f"  - Email: {admin.email}")
            print(f"  - Nombre completo: {admin.first_name} {admin.last_name}")
        else:
            print("  ⚠ Usuario admin no tiene perfil")
            # Crear perfil
            perfil = PerfilUsuario.objects.create(
                user=admin,
                rol='SUPER_ADMIN',
                activo=True
            )
            print("  ✓ Perfil creado automáticamente")
        
        return True
    except User.DoesNotExist:
        print("✗ Usuario admin NO encontrado")
        print("  Crea el usuario con: python manage.py shell")
        return False
    except Exception as e:
        print(f"✗ Error verificando usuario admin: {e}")
        return False

def test_authentication():
    """Prueba la autenticación del usuario admin."""
    try:
        from django.contrib.auth import authenticate
        user = authenticate(username='admin', password='admin123')
        
        if user:
            print(f"✓ Autenticación exitosa para usuario: {user.username}")
            return True
        else:
            print("✗ Autenticación falló - contraseña incorrecta")
            return False
    except Exception as e:
        print(f"✗ Error en autenticación: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("VERIFICACIÓN DEL SISTEMA DE AUTENTICACIÓN")
    print("=" * 60)
    print()
    
    print("1. Verificando conexión a base de datos...")
    db_ok = test_database_connection()
    print()
    
    if db_ok:
        print("2. Verificando usuario admin...")
        admin_ok = test_admin_user()
        print()
        
        if admin_ok:
            print("3. Probando autenticación...")
            auth_ok = test_authentication()
            print()
            
            if auth_ok:
                print("=" * 60)
                print("✓ TODAS LAS VERIFICACIONES PASARON")
                print("=" * 60)
                print("\nEl sistema está listo para usar.")
                print("Puedes hacer login con:")
                print("  username: admin")
                print("  password: admin123")
            else:
                print("=" * 60)
                print("✗ AUTENTICACIÓN FALLÓ")
                print("=" * 60)
        else:
            print("=" * 60)
            print("✗ USUARIO ADMIN NO CONFIGURADO")
            print("=" * 60)
    else:
        print("=" * 60)
        print("✗ ERROR DE CONEXIÓN A BASE DE DATOS")
        print("=" * 60)
        print("\nVerifica:")
        print("1. Que las variables de entorno estén configuradas en Azure")
        print("2. Que la base de datos esté accesible")
