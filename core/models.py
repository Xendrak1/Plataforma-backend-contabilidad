from django.db import models

class Condominio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    ciudad = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "condominios"
        managed = False

class CategoriaVivienda(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    habitaciones = models.SmallIntegerField()
    banos = models.SmallIntegerField()
    churrasquera = models.BooleanField(default=False)
    pisos = models.SmallIntegerField(default=1)
    cochera = models.SmallIntegerField(default=0)
    jardin = models.BooleanField(default=False)
    balcon = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "categorias_vivienda"
        managed = False

class Vivienda(models.Model):
    id = models.BigAutoField(primary_key=True)
    categoria = models.ForeignKey(CategoriaVivienda, on_delete=models.CASCADE, db_column="categoria_id")
    codigo = models.TextField(unique=True)
    metros2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ubicacion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = "viviendas"
        managed = False

class Persona(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombres = models.TextField()
    apellidos = models.TextField()
    num_doc = models.TextField(unique=True)
    telefono = models.TextField(blank=True, null=True)
    email = models.TextField(unique=True, blank=True, null=True)

    class Meta:
        db_table = "personas"
        managed = False

class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, db_column="persona_id")
    email_login = models.TextField(unique=True)
    hash_password = models.TextField()
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "usuarios"
        managed = False

class Rol(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()  # rol_tipo

    class Meta:
        db_table = "roles"
        managed = False

class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column="usuario_id")
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column="rol_id")

    class Meta:
        db_table = "usuario_roles"
        managed = False
        unique_together = (("usuario", "rol"),)

class ResidenteVivienda(models.Model):
    id = models.BigAutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column="persona_id")
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column="vivienda_id")
    es_propietario = models.BooleanField(default=False)
    inicio = models.DateField()
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = "residente_vivienda"
        managed = False

class TipoVehiculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(unique=True)

    class Meta:
        db_table = "tipos_vehiculo"
        managed = False

class Vehiculo(models.Model):
    id = models.BigAutoField(primary_key=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column="persona_id")
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column="vivienda_id")
    tipo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE, db_column="tipo_id")
    placa = models.TextField(unique=True)
    modelo = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "vehiculos"
        managed = False

class Parqueo(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.TextField(unique=True)
    ocupado = models.BooleanField(default=True)

    class Meta:
        db_table = "parqueos"
        managed = False

class ParqueoUsuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    parqueo = models.ForeignKey(Parqueo, on_delete=models.CASCADE, db_column="parqueo_id")
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column="vivienda_id")
    tipo = models.TextField()
    fecha_reserva = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "parqueos_usuario"
        managed = False

class Visitante(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombres = models.TextField()
    apellidos = models.TextField(blank=True, null=True)
    num_doc = models.TextField(blank=True, null=True)
    foto_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "visitantes"
        managed = False

class Visita(models.Model):
    id = models.BigAutoField(primary_key=True)
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, db_column="visitante_id")
    vivienda_destino = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column="vivienda_destino_id")
    entrada = models.DateTimeField()
    salida = models.DateTimeField(blank=True, null=True)
    medio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "visitas"
        managed = False

class AreaComun(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    requiere_pago = models.BooleanField(default=False)
    tarifa = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    reglas = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "areas_comunes"
        managed = False

class Reserva(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.TextField()
    area = models.ForeignKey(AreaComun, on_delete=models.CASCADE, db_column="area_id")
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column="vivienda_id")
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column="persona_id")
    fecha = models.DateField(blank=True, null=True)
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    estado = models.TextField(blank=True, null=True)  # reserva_estado
    qr_reserva = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "reservas"
        managed = False

class ExpensaParametro(models.Model):
    metodo = models.TextField()  # POR_CASA / POR_M2
    tarifa_por_casa = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    tarifa_por_m2 = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    dia_vencimiento = models.SmallIntegerField(blank=True, null=True)
    multa_diaria = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = "expensas_parametros"
        managed = False

class Expensa(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.TextField()
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column="vivienda_id")
    periodo = models.CharField(max_length=7)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    vencimiento = models.DateField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # expensa_estado

    class Meta:
        db_table = "expensas"
        managed = False

class TipoInfraccion(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.TextField(unique=True)
    descripcion = models.TextField(blank=True, null=True)
    monto_base = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "tipos_infraccion"
        managed = False

class Multa(models.Model):
    id = models.BigAutoField(primary_key=True)
    codigo = models.TextField()
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column="vivienda_id")
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column="persona_id")
    tipo_infraccion = models.ForeignKey(TipoInfraccion, on_delete=models.CASCADE, db_column="tipo_infraccion_id")
    fecha = models.DateTimeField(blank=True, null=True)
    evidencia_url = models.TextField(blank=True, null=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # multa_estado

    class Meta:
        db_table = "multas"
        managed = False

class Pago(models.Model):
    id = models.BigAutoField(primary_key=True)
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column="vivienda_id")
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column="persona_id")
    concepto = models.TextField()  # pago_concepto
    referencia_cod = models.BigIntegerField(blank=True, null=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(blank=True, null=True)
    metodo = models.TextField()  # pago_metodo
    estado = models.TextField()  # pago_estado
    qr_payload = models.TextField(blank=True, null=True)
    comprobante_url = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "pagos"
        managed = False

class Comunicado(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.TextField()
    cuerpo = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateTimeField(blank=True, null=True)
    publico = models.TextField(blank=True, null=True)  # TODOS, RESIDENTES, PROPIETARIOS, GUARDIAS

    class Meta:
        db_table = "comunicados"
        managed = False

class LecturaComunicado(models.Model):
    comunicado = models.ForeignKey(Comunicado, on_delete=models.CASCADE, db_column="comunicado_id")
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column="persona_id")
    leido_en = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "lecturas_comunicado"
        managed = False
        unique_together = (("comunicado", "persona"),)

class Mascota(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField()
    tipo = models.TextField()
    raza = models.TextField(blank=True, null=True)
    edad = models.SmallIntegerField(blank=True, null=True)
    propietario = models.ForeignKey(Persona, on_delete=models.CASCADE, db_column="propietario_id")
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, db_column="vivienda_id")

    class Meta:
        db_table = "mascotas"
        managed = False

class AsignacionParqueo(models.Model):
    id = models.BigAutoField(primary_key=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, db_column="vehiculo_id")
    parqueo = models.ForeignKey(Parqueo, on_delete=models.CASCADE, db_column="parqueo_id")
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = "asignaciones_parqueo"
        managed = False

class Notificacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    titulo = models.TextField()
    mensaje = models.TextField()
    tipo = models.TextField()
    prioridad = models.TextField(default='MEDIA')
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "notificaciones"
        managed = False