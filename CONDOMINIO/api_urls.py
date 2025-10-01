from django.urls import path
from core import views

urlpatterns = [
    # Endpoints específicos para cada módulo
    # Residentes
    path('residentes/', views.listar_residentes, name='listar_residentes'),
    path('residentes/crear/', views.crear_residente, name='crear_residente'),
    path('residentes/<int:pk>/', views.detalle_residente, name='detalle_residente'),
    path('residentes/<int:pk>/modificar/', views.modificar_residente, name='modificar_residente'),
    path('residentes/<int:pk>/eliminar/', views.eliminar_residente, name='eliminar_residente'),
    
    # Viviendas
    path('viviendas/', views.listar_viviendas, name='listar_viviendas'),
    path('viviendas/crear/', views.crear_vivienda, name='crear_vivienda'),
    path('viviendas/<int:pk>/', views.detalle_vivienda, name='detalle_vivienda'),
    path('viviendas/<int:pk>/modificar/', views.modificar_vivienda, name='modificar_vivienda'),
    path('viviendas/<int:pk>/eliminar/', views.eliminar_vivienda, name='eliminar_vivienda'),
    
    # Parqueos
    path('parqueos/', views.listar_parqueos, name='listar_parqueos'),
    path('parqueos/crear/', views.crear_parqueo, name='crear_parqueo'),
    path('parqueos/<int:pk>/', views.detalle_parqueo, name='detalle_parqueo'),
    path('parqueos/<int:pk>/modificar/', views.modificar_parqueo, name='modificar_parqueo'),
    path('parqueos/<int:pk>/eliminar/', views.eliminar_parqueo, name='eliminar_parqueo'),
    
    # Visitantes
    path('visitantes/', views.listar_visitantes, name='listar_visitantes'),
    path('visitantes/crear/', views.crear_visitante, name='crear_visitante'),
    path('visitantes/<int:pk>/', views.detalle_visitante, name='detalle_visitante'),
    path('visitantes/<int:pk>/modificar/', views.modificar_visitante, name='modificar_visitante'),
    path('visitantes/<int:pk>/eliminar/', views.eliminar_visitante, name='eliminar_visitante'),
    
    # Control de Visitas
    path('visitas/', views.listar_visitas, name='listar_visitas'),
    path('visitas/registrar-entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('visitas/<int:pk>/registrar-salida/', views.registrar_salida, name='registrar_salida'),
    
    # Reservas
    path('reservas/', views.listar_reservas, name='listar_reservas'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/<int:pk>/', views.detalle_reserva, name='detalle_reserva'),
    path('reservas/<int:pk>/modificar/', views.modificar_reserva, name='modificar_reserva'),
    path('reservas/<int:pk>/eliminar/', views.eliminar_reserva, name='eliminar_reserva'),
    
    # Áreas Comunes
    path('areas/', views.listar_areas, name='listar_areas'),
    path('areas/crear/', views.crear_area, name='crear_area'),
    path('areas/<int:pk>/', views.detalle_area, name='detalle_area'),
    path('areas/<int:pk>/modificar/', views.modificar_area, name='modificar_area'),
    path('areas/<int:pk>/eliminar/', views.eliminar_area, name='eliminar_area'),
    
    # Expensas
    path('expensas/', views.listar_expensas, name='listar_expensas'),
    path('expensas/crear/', views.crear_expensa, name='crear_expensa'),
    path('expensas/<int:pk>/', views.detalle_expensa, name='detalle_expensa'),
    path('expensas/<int:pk>/modificar/', views.modificar_expensa, name='modificar_expensa'),
    path('expensas/<int:pk>/eliminar/', views.eliminar_expensa, name='eliminar_expensa'),
    
    # Pagos
    path('pagos/', views.listar_pagos, name='listar_pagos'),
    path('pagos/crear/', views.crear_pago, name='crear_pago'),
    path('pagos/<int:pk>/', views.detalle_pago, name='detalle_pago'),
    path('pagos/<int:pk>/modificar/', views.modificar_pago, name='modificar_pago'),
    path('pagos/<int:pk>/eliminar/', views.eliminar_pago, name='eliminar_pago'),
    
    # Multas
    path('multas/', views.listar_multas, name='listar_multas'),
    path('multas/crear/', views.crear_multa, name='crear_multa'),
    path('multas/<int:pk>/', views.detalle_multa, name='detalle_multa'),
    path('multas/<int:pk>/modificar/', views.modificar_multa, name='modificar_multa'),
    path('multas/<int:pk>/eliminar/', views.eliminar_multa, name='eliminar_multa'),
    
    # Comunicados
    path('comunicados/', views.listar_comunicados, name='listar_comunicados'),
    path('comunicados/crear/', views.crear_comunicado, name='crear_comunicado'),
    path('comunicados/<int:pk>/', views.detalle_comunicado, name='detalle_comunicado'),
    path('comunicados/<int:pk>/modificar/', views.modificar_comunicado, name='modificar_comunicado'),
    path('comunicados/<int:pk>/eliminar/', views.eliminar_comunicado, name='eliminar_comunicado'),
    path('comunicados/<int:pk>/marcar-leido/', views.marcar_comunicado_leido, name='marcar_comunicado_leido'),
    
    # Vehículos
    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('vehiculos/crear/', views.crear_vehiculo, name='crear_vehiculo'),
    path('vehiculos/<int:pk>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    path('vehiculos/<int:pk>/modificar/', views.modificar_vehiculo, name='modificar_vehiculo'),
    path('vehiculos/<int:pk>/eliminar/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    
    # Tipos de Vehículo
    path('tipos-vehiculo/', views.listar_tipos_vehiculo, name='listar_tipos_vehiculo'),
    path('tipos-vehiculo/crear/', views.crear_tipo_vehiculo, name='crear_tipo_vehiculo'),
    path('tipos-vehiculo/<int:pk>/', views.detalle_tipo_vehiculo, name='detalle_tipo_vehiculo'),
    path('tipos-vehiculo/<int:pk>/modificar/', views.modificar_tipo_vehiculo, name='modificar_tipo_vehiculo'),
    path('tipos-vehiculo/<int:pk>/eliminar/', views.eliminar_tipo_vehiculo, name='eliminar_tipo_vehiculo'),
    
    # Mascotas
    path('mascotas/', views.listar_mascotas, name='listar_mascotas'),
    path('mascotas/crear/', views.crear_mascota, name='crear_mascota'),
    path('mascotas/<int:pk>/', views.detalle_mascota, name='detalle_mascota'),
    path('mascotas/<int:pk>/modificar/', views.modificar_mascota, name='modificar_mascota'),
    path('mascotas/<int:pk>/eliminar/', views.eliminar_mascota, name='eliminar_mascota'),
    
    # Asignación de Parqueos (DESHABILITADO - requiere tabla asignaciones_parqueo)
    # path('asignaciones-parqueo/', views.listar_asignaciones_parqueo, name='listar_asignaciones_parqueo'),
    # path('asignaciones-parqueo/crear/', views.crear_asignacion_parqueo, name='crear_asignacion_parqueo'),
    # path('asignaciones-parqueo/<int:pk>/', views.detalle_asignacion_parqueo, name='detalle_asignacion_parqueo'),
    # path('asignaciones-parqueo/<int:pk>/modificar/', views.modificar_asignacion_parqueo, name='modificar_asignacion_parqueo'),
    # path('asignaciones-parqueo/<int:pk>/eliminar/', views.eliminar_asignacion_parqueo, name='eliminar_asignacion_parqueo'),
    # path('parqueos/disponibles/', views.parqueos_disponibles, name='parqueos_disponibles'),
    
    # Reportes y Análisis
    path('reportes/resumen-general/', views.reporte_resumen_general, name='reporte_resumen_general'),
    path('reportes/expensas/', views.reporte_expensas, name='reporte_expensas'),
    path('reportes/visitas/', views.reporte_visitas, name='reporte_visitas'),
    # path('reportes/vehiculos/', views.reporte_vehiculos, name='reporte_vehiculos'),  # DESHABILITADO
    # path('reportes/ocupacion-parqueos/', views.reporte_ocupacion_parqueos, name='reporte_ocupacion_parqueos'),  # DESHABILITADO
    # path('reportes/estadisticas-mensuales/', views.estadisticas_mensuales, name='estadisticas_mensuales'),  # DESHABILITADO
    
    # Notificaciones (DESHABILITADO - requiere tabla notificaciones)
    # path('notificaciones/', views.listar_notificaciones, name='listar_notificaciones'),
    # path('notificaciones/crear/', views.crear_notificacion, name='crear_notificacion'),
    # path('notificaciones/<int:pk>/marcar-leida/', views.marcar_notificacion_leida, name='marcar_notificacion_leida'),
    # path('notificaciones/alertas/', views.alertas_automaticas, name='alertas_automaticas'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Endpoints genéricos (mantener para compatibilidad)
    path('<str:model_name>/', views.listar, name='listar'),
    path('<str:model_name>/crear/', views.crear, name='crear'),
    path('<str:model_name>/<int:pk>/modificar/', views.modificar, name='modificar'),
    path('<str:model_name>/<int:pk>/eliminar/', views.eliminar, name='eliminar'),
]
