"""
Script para configurar el usuario administrador inicial después de la migración.
Este script debe ejecutarse DESPUÉS de las migraciones.
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONDOMINIO.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario

def setup_admin():
    """Crea o actualiza el usuario administrador."""
    
    print("🔧 Configurando usuario administrador...")
    
    # Verificar si ya existe un superusuario
    if User.objects.filter(username='admin').exists():
        print("⚠️  Ya existe el usuario 'admin'. Actualizando...")
        admin = User.objects.get(username='admin')
    else:
        # Crear superusuario
        print("📝 Creando superusuario...")
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@condominio.com',
            password='admin123',  # Cambiar en producción
            first_name='Administrador',
            last_name='Sistema'
        )
        print(f"✅ Superusuario creado: {admin.username}")
    
    # Configurar perfil y rol de administrador
    perfil = admin.perfil
    if perfil.rol != 'SUPER_ADMIN':
        perfil.rol = 'SUPER_ADMIN'
        perfil.activo = True
        perfil.save()
        print(f"✅ Rol actualizado a: {perfil.get_rol_display()}")
    
    print("\n" + "="*50)
    print("✅ CONFIGURACIÓN COMPLETADA")
    print("="*50)
    print(f"Usuario: {admin.username}")
    print(f"Email: {admin.email}")
    print(f"Rol: {perfil.get_rol_display()}")
    print(f"Contraseña: admin123 (CAMBIAR EN PRODUCCIÓN)")
    print("="*50)

if __name__ == '__main__':
    setup_admin()
