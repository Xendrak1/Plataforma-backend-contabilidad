from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilUsuario(models.Model):
    """
    Perfil extendido del usuario con información adicional para el condominio.
    """
    
    ROL_CHOICES = [
        ('SUPER_ADMIN', 'Super Administrador'),
        ('ADMIN', 'Administrador'),
        ('CONTADOR', 'Contador'),
        ('GUARDIA', 'Guardia de Seguridad'),
        ('RESIDENTE', 'Residente'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuario'
    )
    
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='RESIDENTE',
        verbose_name='Rol'
    )
    
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    
    vivienda = models.ForeignKey(
        'core.Vivienda',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        verbose_name='Vivienda'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización'
    )
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
        ordering = ['-fecha_creacion']
        db_table = 'perfiles_usuario'
    
    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"
    
    @property
    def nombre_completo(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    def es_admin(self):
        return self.rol in ['SUPER_ADMIN', 'ADMIN']
    
    def es_contador(self):
        return self.rol == 'CONTADOR'
    
    def es_guardia(self):
        return self.rol == 'GUARDIA'
    
    def es_residente(self):
        return self.rol == 'RESIDENTE'


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente un perfil cuando se crea un usuario."""
    if created:
        PerfilUsuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """Guarda el perfil cuando se guarda el usuario."""
    if hasattr(instance, 'perfil'):
        instance.perfil.save()
