from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import PerfilUsuario


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Condominio'
    fields = ('rol', 'telefono', 'vivienda', 'activo')


class UsuarioAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_rol', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    
    def get_rol(self, obj):
        return obj.perfil.get_rol_display() if hasattr(obj, 'perfil') else 'N/A'
    get_rol.short_description = 'Rol'


# Re-registrar UserAdmin
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)

# Registrar PerfilUsuario
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'telefono', 'vivienda', 'activo', 'fecha_creacion']
    list_filter = ['rol', 'activo']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
