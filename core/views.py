from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import *

# ------------------------------
# FUNCIONES GENERALES PARA CRUD
# ------------------------------

def model_to_dict(instance):
    """
    Convierte un objeto de modelo a diccionario, manejando ForeignKeys.
    """
    data = {}
    for field in instance._meta.fields:
        value = getattr(instance, field.name)
        # si es FK, devuelve el id
        if field.is_relation and value is not None:
            value = value.id
        data[field.name] = value
    return data

# ------------------------------
# ENDPOINTS ESPECÍFICOS
# ------------------------------

# RESIDENTES
@csrf_exempt
def listar_residentes(request):
    """Listar todos los residentes con información de vivienda"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    residentes = ResidenteVivienda.objects.select_related('persona', 'vivienda').all()
    data = []
    for res in residentes:
        data.append({
            'id': res.id,
            'persona_id': res.persona.id,
            'nombres': res.persona.nombres,
            'apellidos': res.persona.apellidos,
            'email': res.persona.email,
            'telefono': res.persona.telefono,
            'vivienda_id': res.vivienda.id,
            'codigo_vivienda': res.vivienda.codigo,
            'es_propietario': res.es_propietario,
            'estado': res.estado
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_residente(request):
    """Crear un nuevo residente"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body)
    try:
        # Crear persona primero
        persona = Persona.objects.create(
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            num_doc=data['num_doc'],
            telefono=data.get('telefono', ''),
            email=data.get('email', '')
        )
        
        # Crear relación residente-vivienda
        residente = ResidenteVivienda.objects.create(
            persona=persona,
            vivienda_id=data['vivienda_id'],
            es_propietario=data.get('es_propietario', False),
            inicio=data.get('inicio', '2025-01-01'),
            estado=True
        )
        
        return JsonResponse({
            'id': residente.id,
            'persona_id': persona.id,
            'nombres': persona.nombres,
            'apellidos': persona.apellidos,
            'email': persona.email,
            'telefono': persona.telefono,
            'vivienda_id': residente.vivienda.id,
            'es_propietario': residente.es_propietario,
            'estado': residente.estado
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def detalle_residente(request, pk):
    """Obtener detalles de un residente"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    residente = get_object_or_404(ResidenteVivienda, pk=pk)
    return JsonResponse({
        'id': residente.id,
        'persona_id': residente.persona.id,
        'nombres': residente.persona.nombres,
        'apellidos': residente.persona.apellidos,
        'email': residente.persona.email,
        'telefono': residente.persona.telefono,
        'vivienda_id': residente.vivienda.id,
        'codigo_vivienda': residente.vivienda.codigo,
        'es_propietario': residente.es_propietario,
        'estado': residente.estado
    })

@csrf_exempt
def modificar_residente(request, pk):
    """Modificar un residente"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    residente = get_object_or_404(ResidenteVivienda, pk=pk)
    data = json.loads(request.body)
    
    # Actualizar persona
    if 'nombres' in data:
        residente.persona.nombres = data['nombres']
    if 'apellidos' in data:
        residente.persona.apellidos = data['apellidos']
    if 'email' in data:
        residente.persona.email = data['email']
    if 'telefono' in data:
        residente.persona.telefono = data['telefono']
    residente.persona.save()
    
    # Actualizar residente
    if 'vivienda_id' in data:
        residente.vivienda_id = data['vivienda_id']
    if 'es_propietario' in data:
        residente.es_propietario = data['es_propietario']
    if 'estado' in data:
        residente.estado = data['estado']
    residente.save()
    
    return JsonResponse({
        'id': residente.id,
        'persona_id': residente.persona.id,
        'nombres': residente.persona.nombres,
        'apellidos': residente.persona.apellidos,
        'email': residente.persona.email,
        'telefono': residente.persona.telefono,
        'vivienda_id': residente.vivienda.id,
        'es_propietario': residente.es_propietario,
        'estado': residente.estado
    })

@csrf_exempt
def eliminar_residente(request, pk):
    """Eliminar un residente"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    residente = get_object_or_404(ResidenteVivienda, pk=pk)
    residente.delete()
    return JsonResponse({"status": "ok"})

# VIVIENDAS
@csrf_exempt
def listar_viviendas(request):
    """Listar todas las viviendas"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    viviendas = Vivienda.objects.select_related('categoria').all()
    data = []
    for v in viviendas:
        data.append({
            'id': v.id,
            'codigo': v.codigo,
            'metros2': float(v.metros2) if v.metros2 else None,
            'ubicacion': v.ubicacion,
            'activo': v.activo,
            'categoria_id': v.categoria.id,
            'categoria_nombre': v.categoria.nombre,
            'habitaciones': v.categoria.habitaciones,
            'banos': v.categoria.banos
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_vivienda(request):
    """Crear una nueva vivienda"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body)
    try:
        vivienda = Vivienda.objects.create(
            categoria_id=data['categoria_id'],
            codigo=data['codigo'],
            metros2=data.get('metros2'),
            ubicacion=data.get('ubicacion', ''),
            activo=data.get('activo', True)
        )
        return JsonResponse(model_to_dict(vivienda))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def detalle_vivienda(request, pk):
    """Obtener detalles de una vivienda"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    vivienda = get_object_or_404(Vivienda, pk=pk)
    return JsonResponse(model_to_dict(vivienda))

@csrf_exempt
def modificar_vivienda(request, pk):
    """Modificar una vivienda"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    vivienda = get_object_or_404(Vivienda, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(vivienda, key, value)
    vivienda.save()
    return JsonResponse(model_to_dict(vivienda))

@csrf_exempt
def eliminar_vivienda(request, pk):
    """Eliminar una vivienda"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    vivienda = get_object_or_404(Vivienda, pk=pk)
    vivienda.delete()
    return JsonResponse({"status": "ok"})

# PARQUEOS
@csrf_exempt
def listar_parqueos(request):
    """Listar todos los parqueos"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    parqueos = Parqueo.objects.all()
    data = [model_to_dict(p) for p in parqueos]
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_parqueo(request):
    """Crear un nuevo parqueo"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body)
    try:
        parqueo = Parqueo.objects.create(**data)
        return JsonResponse(model_to_dict(parqueo))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def detalle_parqueo(request, pk):
    """Obtener detalles de un parqueo"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    parqueo = get_object_or_404(Parqueo, pk=pk)
    return JsonResponse(model_to_dict(parqueo))

@csrf_exempt
def modificar_parqueo(request, pk):
    """Modificar un parqueo"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    parqueo = get_object_or_404(Parqueo, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(parqueo, key, value)
    parqueo.save()
    return JsonResponse(model_to_dict(parqueo))

@csrf_exempt
def eliminar_parqueo(request, pk):
    """Eliminar un parqueo"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    parqueo = get_object_or_404(Parqueo, pk=pk)
    parqueo.delete()
    return JsonResponse({"status": "ok"})

# VISITANTES
@csrf_exempt
def listar_visitantes(request):
    """Listar todos los visitantes con información de visitas"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    visitantes = Visitante.objects.all().order_by('-id')
    data = []
    for visitante in visitantes:
        # Obtener la última visita
        ultima_visita = Visita.objects.filter(visitante=visitante).order_by('-entrada').first()
        
        data.append({
            'id': visitante.id,
            'nombres': visitante.nombres,
            'apellidos': visitante.apellidos,
            'num_doc': visitante.num_doc,
            'foto_url': visitante.foto_url,
            'ultima_visita': ultima_visita.entrada.isoformat() if ultima_visita else None,
            'estado_visita': 'En el condominio' if ultima_visita and not ultima_visita.salida else 'Fuera'
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_visitante(request):
    """Crear un nuevo visitante"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validar campos requeridos
        if 'nombres' not in data:
            return JsonResponse({"error": "Campo requerido: nombres"}, status=400)
        
        # Crear el visitante
        visitante = Visitante.objects.create(
            nombres=data['nombres'],
            apellidos=data.get('apellidos', ''),
            num_doc=data.get('num_doc', ''),
            foto_url=data.get('foto_url', '')
        )
        
        return JsonResponse({
            'id': visitante.id,
            'nombres': visitante.nombres,
            'apellidos': visitante.apellidos,
            'num_doc': visitante.num_doc,
            'foto_url': visitante.foto_url,
            'ultima_visita': None,
            'estado_visita': 'Fuera'
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def detalle_visitante(request, pk):
    """Obtener detalles de un visitante"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    visitante = get_object_or_404(Visitante, pk=pk)
    return JsonResponse(model_to_dict(visitante))

@csrf_exempt
def modificar_visitante(request, pk):
    """Modificar un visitante"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    visitante = get_object_or_404(Visitante, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(visitante, key, value)
    visitante.save()
    return JsonResponse(model_to_dict(visitante))

@csrf_exempt
def eliminar_visitante(request, pk):
    """Eliminar un visitante"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        visitante = get_object_or_404(Visitante, pk=pk)
        visitante.delete()
        return JsonResponse({"message": "Visitante eliminado correctamente"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ------------------------------
# CONTROL DE VISITAS
# ------------------------------

@csrf_exempt
def registrar_entrada(request):
    """Registrar entrada de un visitante"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validar campos requeridos
        required_fields = ['visitante_id', 'vivienda_destino_id']
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"Campo requerido: {field}"}, status=400)
        
        # Verificar que el visitante existe
        visitante = get_object_or_404(Visitante, id=data['visitante_id'])
        
        # Verificar que la vivienda existe
        vivienda = get_object_or_404(Vivienda, id=data['vivienda_destino_id'])
        
        # Crear la visita
        visita = Visita.objects.create(
            visitante=visitante,
            vivienda_destino=vivienda,
            entrada=timezone.now(),
            medio=data.get('medio', '')
        )
        
        return JsonResponse({
            'id': visita.id,
            'visitante_id': visita.visitante.id,
            'visitante_nombre': f"{visita.visitante.nombres} {visita.visitante.apellidos}",
            'vivienda_destino_id': visita.vivienda_destino.id,
            'codigo_vivienda': visita.vivienda_destino.codigo,
            'entrada': visita.entrada.isoformat(),
            'salida': visita.salida.isoformat() if visita.salida else None,
            'medio': visita.medio
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def registrar_salida(request, pk):
    """Registrar salida de un visitante"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        visita = get_object_or_404(Visita, id=pk)
        
        if visita.salida:
            return JsonResponse({"error": "El visitante ya registró su salida"}, status=400)
        
        visita.salida = timezone.now()
        visita.save()
        
        return JsonResponse({
            'id': visita.id,
            'visitante_id': visita.visitante.id,
            'visitante_nombre': f"{visita.visitante.nombres} {visita.visitante.apellidos}",
            'vivienda_destino_id': visita.vivienda_destino.id,
            'codigo_vivienda': visita.vivienda_destino.codigo,
            'entrada': visita.entrada.isoformat(),
            'salida': visita.salida.isoformat(),
            'medio': visita.medio
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def listar_visitas(request):
    """Listar todas las visitas con información detallada"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    visitas = Visita.objects.select_related('visitante', 'vivienda_destino').all().order_by('-entrada')
    data = []
    for visita in visitas:
        data.append({
            'id': visita.id,
            'visitante_id': visita.visitante.id,
            'visitante_nombre': f"{visita.visitante.nombres} {visita.visitante.apellidos}",
            'vivienda_destino_id': visita.vivienda_destino.id,
            'codigo_vivienda': visita.vivienda_destino.codigo,
            'entrada': visita.entrada.isoformat(),
            'salida': visita.salida.isoformat() if visita.salida else None,
            'medio': visita.medio,
            'estado': 'En el condominio' if not visita.salida else 'Salido'
        })
    return JsonResponse(data, safe=False)

# RESERVAS
@csrf_exempt
def listar_reservas(request):
    """Listar todas las reservas"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    reservas = Reserva.objects.select_related('area', 'vivienda', 'persona').all()
    data = []
    for r in reservas:
        data.append({
            'id': r.id,
            'codigo': r.codigo,
            'area_id': r.area.id,
            'area_nombre': r.area.nombre,
            'vivienda_id': r.vivienda.id,
            'codigo_vivienda': r.vivienda.codigo,
            'persona_id': r.persona.id,
            'persona_nombre': f"{r.persona.nombres} {r.persona.apellidos}",
            'fecha': r.fecha,
            'hora_inicio': r.hora_inicio,
            'hora_fin': r.hora_fin,
            'estado': r.estado
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_reserva(request):
    """Crear una nueva reserva"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body)
    try:
        reserva = Reserva.objects.create(**data)
        return JsonResponse(model_to_dict(reserva))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def detalle_reserva(request, pk):
    """Obtener detalles de una reserva"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    reserva = get_object_or_404(Reserva, pk=pk)
    return JsonResponse(model_to_dict(reserva))

@csrf_exempt
def modificar_reserva(request, pk):
    """Modificar una reserva"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    reserva = get_object_or_404(Reserva, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(reserva, key, value)
    reserva.save()
    return JsonResponse(model_to_dict(reserva))

@csrf_exempt
def eliminar_reserva(request, pk):
    """Eliminar una reserva"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.delete()
    return JsonResponse({"status": "ok"})

# ÁREAS COMUNES
@csrf_exempt
def listar_areas(request):
    """Listar todas las áreas comunes"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    areas = AreaComun.objects.all()
    data = [model_to_dict(a) for a in areas]
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_area(request):
    """Crear una nueva área común"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body)
    try:
        area = AreaComun.objects.create(**data)
        return JsonResponse(model_to_dict(area))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def detalle_area(request, pk):
    """Obtener detalles de un área común"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    area = get_object_or_404(AreaComun, pk=pk)
    return JsonResponse(model_to_dict(area))

@csrf_exempt
def modificar_area(request, pk):
    """Modificar un área común"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    area = get_object_or_404(AreaComun, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(area, key, value)
    area.save()
    return JsonResponse(model_to_dict(area))

@csrf_exempt
def eliminar_area(request, pk):
    """Eliminar un área común"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    area = get_object_or_404(AreaComun, pk=pk)
    area.delete()
    return JsonResponse({"status": "ok"})

# EXPENSAS
@csrf_exempt
def listar_expensas(request):
    """Listar todas las expensas"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    expensas = Expensa.objects.select_related('vivienda').all()
    data = []
    for e in expensas:
        data.append({
            'id': e.id,
            'codigo': e.codigo,
            'vivienda_id': e.vivienda.id,
            'codigo_vivienda': e.vivienda.codigo,
            'periodo': e.periodo,
            'monto': float(e.monto),
            'vencimiento': e.vencimiento,
            'estado': e.estado
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_expensa(request):
    """Crear una nueva expensa"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body)
    try:
        expensa = Expensa.objects.create(**data)
        return JsonResponse(model_to_dict(expensa))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def detalle_expensa(request, pk):
    """Obtener detalles de una expensa"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    expensa = get_object_or_404(Expensa, pk=pk)
    return JsonResponse(model_to_dict(expensa))

@csrf_exempt
def modificar_expensa(request, pk):
    """Modificar una expensa"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    expensa = get_object_or_404(Expensa, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(expensa, key, value)
    expensa.save()
    return JsonResponse(model_to_dict(expensa))

@csrf_exempt
def eliminar_expensa(request, pk):
    """Eliminar una expensa"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    expensa = get_object_or_404(Expensa, pk=pk)
    expensa.delete()
    return JsonResponse({"status": "ok"})

# PAGOS
@csrf_exempt
def listar_pagos(request):
    """Listar todos los pagos"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    pagos = Pago.objects.select_related('vivienda', 'persona').all()
    data = []
    for p in pagos:
        data.append({
            'id': p.id,
            'vivienda_id': p.vivienda.id,
            'codigo_vivienda': p.vivienda.codigo,
            'persona_id': p.persona.id,
            'persona_nombre': f"{p.persona.nombres} {p.persona.apellidos}",
            'concepto': p.concepto,
            'monto': float(p.monto),
            'fecha': p.fecha,
            'metodo': p.metodo,
            'estado': p.estado
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_pago(request):
    """Crear un nuevo pago"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body)
    try:
        pago = Pago.objects.create(**data)
        return JsonResponse(model_to_dict(pago))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def detalle_pago(request, pk):
    """Obtener detalles de un pago"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    pago = get_object_or_404(Pago, pk=pk)
    return JsonResponse(model_to_dict(pago))

@csrf_exempt
def modificar_pago(request, pk):
    """Modificar un pago"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    pago = get_object_or_404(Pago, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(pago, key, value)
    pago.save()
    return JsonResponse(model_to_dict(pago))

@csrf_exempt
def eliminar_pago(request, pk):
    """Eliminar un pago"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    pago = get_object_or_404(Pago, pk=pk)
    pago.delete()
    return JsonResponse({"status": "ok"})

# MULTAS
@csrf_exempt
def listar_multas(request):
    """Listar todas las multas"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    multas = Multa.objects.select_related('vivienda', 'persona', 'tipo_infraccion').all()
    data = []
    for m in multas:
        data.append({
            'id': m.id,
            'codigo': m.codigo,
            'vivienda_id': m.vivienda.id,
            'codigo_vivienda': m.vivienda.codigo,
            'persona_id': m.persona.id,
            'persona_nombre': f"{m.persona.nombres} {m.persona.apellidos}",
            'tipo_infraccion_id': m.tipo_infraccion.id,
            'tipo_infraccion_descripcion': m.tipo_infraccion.descripcion,
            'fecha': m.fecha,
            'monto': float(m.monto) if m.monto else None,
            'estado': m.estado
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_multa(request):
    """Crear una nueva multa"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    data = json.loads(request.body)
    try:
        multa = Multa.objects.create(**data)
        return JsonResponse(model_to_dict(multa))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def detalle_multa(request, pk):
    """Obtener detalles de una multa"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    multa = get_object_or_404(Multa, pk=pk)
    return JsonResponse(model_to_dict(multa))

@csrf_exempt
def modificar_multa(request, pk):
    """Modificar una multa"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    multa = get_object_or_404(Multa, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(multa, key, value)
    multa.save()
    return JsonResponse(model_to_dict(multa))

@csrf_exempt
def eliminar_multa(request, pk):
    """Eliminar una multa"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    multa = get_object_or_404(Multa, pk=pk)
    multa.delete()
    return JsonResponse({"status": "ok"})

# COMUNICADOS
@csrf_exempt
def listar_comunicados(request):
    """Listar todos los comunicados con información de lecturas"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    comunicados = Comunicado.objects.all().order_by('-fecha_publicacion')
    data = []
    for com in comunicados:
        # Contar lecturas
        total_lecturas = LecturaComunicado.objects.filter(comunicado=com).count()
        
        data.append({
            'id': com.id,
            'titulo': com.titulo,
            'cuerpo': com.cuerpo,
            'fecha_publicacion': com.fecha_publicacion.isoformat() if com.fecha_publicacion else None,
            'publico': com.publico,
            'total_lecturas': total_lecturas
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_comunicado(request):
    """Crear un nuevo comunicado"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validar campos requeridos
        if 'titulo' not in data:
            return JsonResponse({"error": "Campo requerido: titulo"}, status=400)
        
        # Crear el comunicado
        comunicado = Comunicado.objects.create(
            titulo=data['titulo'],
            cuerpo=data.get('cuerpo', ''),
            publico=data.get('publico', 'TODOS')
        )
        
        return JsonResponse({
            'id': comunicado.id,
            'titulo': comunicado.titulo,
            'cuerpo': comunicado.cuerpo,
            'fecha_publicacion': comunicado.fecha_publicacion.isoformat() if comunicado.fecha_publicacion else None,
            'publico': comunicado.publico,
            'total_lecturas': 0
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def detalle_comunicado(request, pk):
    """Obtener detalles de un comunicado con información de lecturas"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        comunicado = get_object_or_404(Comunicado, pk=pk)
        
        # Obtener lecturas
        lecturas = LecturaComunicado.objects.filter(comunicado=comunicado).select_related('persona')
        lecturas_data = []
        for lectura in lecturas:
            lecturas_data.append({
                'persona_id': lectura.persona.id,
                'persona_nombre': f"{lectura.persona.nombres} {lectura.persona.apellidos}",
                'leido_en': lectura.leido_en.isoformat() if lectura.leido_en else None
            })
        
        return JsonResponse({
            'id': comunicado.id,
            'titulo': comunicado.titulo,
            'cuerpo': comunicado.cuerpo,
            'fecha_publicacion': comunicado.fecha_publicacion.isoformat() if comunicado.fecha_publicacion else None,
            'publico': comunicado.publico,
            'total_lecturas': len(lecturas_data),
            'lecturas': lecturas_data
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def modificar_comunicado(request, pk):
    """Modificar un comunicado"""
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    comunicado = get_object_or_404(Comunicado, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(comunicado, key, value)
    comunicado.save()
    return JsonResponse(model_to_dict(comunicado))

@csrf_exempt
def eliminar_comunicado(request, pk):
    """Eliminar un comunicado"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        comunicado = get_object_or_404(Comunicado, pk=pk)
        comunicado.delete()
        return JsonResponse({"message": "Comunicado eliminado correctamente"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def marcar_comunicado_leido(request, pk):
    """Marcar un comunicado como leído por una persona"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        if 'persona_id' not in data:
            return JsonResponse({"error": "Campo requerido: persona_id"}, status=400)
        
        comunicado = get_object_or_404(Comunicado, pk=pk)
        persona = get_object_or_404(Persona, id=data['persona_id'])
        
        # Crear o actualizar la lectura
        lectura, created = LecturaComunicado.objects.get_or_create(
            comunicado=comunicado,
            persona=persona,
            defaults={'leido_en': timezone.now()}
        )
        
        if not created:
            # Si ya existía, actualizar la fecha
            lectura.leido_en = timezone.now()
            lectura.save()
        
        return JsonResponse({
            "message": "Comunicado marcado como leído",
            "leido_en": lectura.leido_en.isoformat()
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# DASHBOARD
@csrf_exempt
def dashboard(request):
    """Obtener datos del dashboard"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    # Estadísticas básicas
    total_residentes = ResidenteVivienda.objects.filter(estado=True).count()
    total_viviendas = Vivienda.objects.filter(activo=True).count()
    total_parqueos = Parqueo.objects.count()
    parqueos_ocupados = Parqueo.objects.filter(ocupado=True).count()
    total_expensas = Expensa.objects.count()
    expensas_pendientes = Expensa.objects.filter(estado='PENDIENTE').count()
    total_multas = Multa.objects.count()
    multas_pendientes = Multa.objects.filter(estado='PENDIENTE').count()
    total_vehiculos = Vehiculo.objects.count()
    total_tipos_vehiculo = TipoVehiculo.objects.count()
    total_mascotas = Mascota.objects.count()
    
    return JsonResponse({
        'residentes': {
            'total': total_residentes
        },
        'viviendas': {
            'total': total_viviendas
        },
        'parqueos': {
            'total': total_parqueos,
            'ocupados': parqueos_ocupados,
            'disponibles': total_parqueos - parqueos_ocupados
        },
        'expensas': {
            'total': total_expensas,
            'pendientes': expensas_pendientes
        },
        'multas': {
            'total': total_multas,
            'pendientes': multas_pendientes
        },
        'vehiculos': {
            'total': total_vehiculos,
            'tipos': total_tipos_vehiculo
        },
        'mascotas': {
            'total': total_mascotas
        }
    })

# ------------------------------
# GESTIÓN DE VEHÍCULOS
# ------------------------------

@csrf_exempt
def listar_vehiculos(request):
    """Listar todos los vehículos con información de propietario y vivienda"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    vehiculos = Vehiculo.objects.select_related('persona', 'vivienda', 'tipo').all()
    data = []
    for veh in vehiculos:
        data.append({
            'id': veh.id,
            'persona_id': veh.persona.id,
            'persona_nombre': f"{veh.persona.nombres} {veh.persona.apellidos}",
            'vivienda_id': veh.vivienda.id,
            'codigo_vivienda': veh.vivienda.codigo,
            'tipo_id': veh.tipo.id,
            'tipo_nombre': veh.tipo.nombre,
            'placa': veh.placa,
            'modelo': veh.modelo,
            'color': veh.color
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_vehiculo(request):
    """Crear un nuevo vehículo"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validar campos requeridos
        required_fields = ['persona_id', 'vivienda_id', 'tipo_id', 'placa']
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"Campo requerido: {field}"}, status=400)
        
        # Verificar que la persona existe
        persona = get_object_or_404(Persona, id=data['persona_id'])
        
        # Verificar que la vivienda existe
        vivienda = get_object_or_404(Vivienda, id=data['vivienda_id'])
        
        # Verificar que el tipo de vehículo existe
        tipo_vehiculo = get_object_or_404(TipoVehiculo, id=data['tipo_id'])
        
        # Crear el vehículo
        vehiculo = Vehiculo.objects.create(
            persona=persona,
            vivienda=vivienda,
            tipo=tipo_vehiculo,
            placa=data['placa'],
            modelo=data.get('modelo', ''),
            color=data.get('color', '')
        )
        
        return JsonResponse({
            'id': vehiculo.id,
            'persona_id': vehiculo.persona.id,
            'persona_nombre': f"{vehiculo.persona.nombres} {vehiculo.persona.apellidos}",
            'vivienda_id': vehiculo.vivienda.id,
            'codigo_vivienda': vehiculo.vivienda.codigo,
            'tipo_id': vehiculo.tipo.id,
            'tipo_nombre': vehiculo.tipo.nombre,
            'placa': vehiculo.placa,
            'modelo': vehiculo.modelo,
            'color': vehiculo.color
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def detalle_vehiculo(request, pk):
    """Obtener detalles de un vehículo específico"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        vehiculo = get_object_or_404(Vehiculo.objects.select_related('persona', 'vivienda', 'tipo'), id=pk)
        
        return JsonResponse({
            'id': vehiculo.id,
            'persona_id': vehiculo.persona.id,
            'persona_nombre': f"{vehiculo.persona.nombres} {vehiculo.persona.apellidos}",
            'vivienda_id': vehiculo.vivienda.id,
            'codigo_vivienda': vehiculo.vivienda.codigo,
            'tipo_id': vehiculo.tipo.id,
            'tipo_nombre': vehiculo.tipo.nombre,
            'placa': vehiculo.placa,
            'modelo': vehiculo.modelo,
            'color': vehiculo.color
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def modificar_vehiculo(request, pk):
    """Modificar un vehículo existente"""
    if request.method not in ["PUT", "PATCH"]:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        vehiculo = get_object_or_404(Vehiculo, id=pk)
        data = json.loads(request.body)
        
        # Actualizar campos si están presentes
        if 'persona_id' in data:
            persona = get_object_or_404(Persona, id=data['persona_id'])
            vehiculo.persona = persona
            
        if 'vivienda_id' in data:
            vivienda = get_object_or_404(Vivienda, id=data['vivienda_id'])
            vehiculo.vivienda = vivienda
            
        if 'tipo_id' in data:
            tipo_vehiculo = get_object_or_404(TipoVehiculo, id=data['tipo_id'])
            vehiculo.tipo = tipo_vehiculo
            
        if 'placa' in data:
            vehiculo.placa = data['placa']
            
        if 'modelo' in data:
            vehiculo.modelo = data['modelo']
            
        if 'color' in data:
            vehiculo.color = data['color']
        
        vehiculo.save()
        
        return JsonResponse({
            'id': vehiculo.id,
            'persona_id': vehiculo.persona.id,
            'persona_nombre': f"{vehiculo.persona.nombres} {vehiculo.persona.apellidos}",
            'vivienda_id': vehiculo.vivienda.id,
            'codigo_vivienda': vehiculo.vivienda.codigo,
            'tipo_id': vehiculo.tipo.id,
            'tipo_nombre': vehiculo.tipo.nombre,
            'placa': vehiculo.placa,
            'modelo': vehiculo.modelo,
            'color': vehiculo.color
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def eliminar_vehiculo(request, pk):
    """Eliminar un vehículo"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        vehiculo = get_object_or_404(Vehiculo, id=pk)
        vehiculo.delete()
        
        return JsonResponse({"message": "Vehículo eliminado correctamente"})
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ------------------------------
# GESTIÓN DE TIPOS DE VEHÍCULO
# ------------------------------

@csrf_exempt
def listar_tipos_vehiculo(request):
    """Listar todos los tipos de vehículo"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    tipos = TipoVehiculo.objects.all()
    data = []
    for tipo in tipos:
        data.append({
            'id': tipo.id,
            'nombre': tipo.nombre
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_tipo_vehiculo(request):
    """Crear un nuevo tipo de vehículo"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        if 'nombre' not in data:
            return JsonResponse({"error": "Campo requerido: nombre"}, status=400)
        
        tipo = TipoVehiculo.objects.create(nombre=data['nombre'])
        
        return JsonResponse({
            'id': tipo.id,
            'nombre': tipo.nombre
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def detalle_tipo_vehiculo(request, pk):
    """Obtener detalles de un tipo de vehículo específico"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        tipo = get_object_or_404(TipoVehiculo, id=pk)
        
        return JsonResponse({
            'id': tipo.id,
            'nombre': tipo.nombre
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def modificar_tipo_vehiculo(request, pk):
    """Modificar un tipo de vehículo existente"""
    if request.method not in ["PUT", "PATCH"]:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        tipo = get_object_or_404(TipoVehiculo, id=pk)
        data = json.loads(request.body)
        
        if 'nombre' in data:
            tipo.nombre = data['nombre']
        
        tipo.save()
        
        return JsonResponse({
            'id': tipo.id,
            'nombre': tipo.nombre
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def eliminar_tipo_vehiculo(request, pk):
    """Eliminar un tipo de vehículo"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        tipo = get_object_or_404(TipoVehiculo, id=pk)
        tipo.delete()
        
        return JsonResponse({"message": "Tipo de vehículo eliminado correctamente"})
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ------------------------------
# GESTIÓN DE MASCOTAS
# ------------------------------

@csrf_exempt
def listar_mascotas(request):
    """Listar todas las mascotas con información de propietario y vivienda"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    mascotas = Mascota.objects.select_related('propietario', 'vivienda').all().order_by('-id')
    data = []
    for mascota in mascotas:
        data.append({
            'id': mascota.id,
            'nombre': mascota.nombre,
            'tipo': mascota.tipo,
            'raza': mascota.raza,
            'edad': mascota.edad,
            'propietario_id': mascota.propietario.id,
            'propietario_nombre': f"{mascota.propietario.nombres} {mascota.propietario.apellidos}",
            'vivienda_id': mascota.vivienda.id,
            'codigo_vivienda': mascota.vivienda.codigo
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_mascota(request):
    """Crear una nueva mascota"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validar campos requeridos
        required_fields = ['nombre', 'tipo', 'propietario_id', 'vivienda_id']
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"Campo requerido: {field}"}, status=400)
        
        # Verificar que el propietario existe
        propietario = get_object_or_404(Persona, id=data['propietario_id'])
        
        # Verificar que la vivienda existe
        vivienda = get_object_or_404(Vivienda, id=data['vivienda_id'])
        
        # Crear la mascota
        mascota = Mascota.objects.create(
            nombre=data['nombre'],
            tipo=data['tipo'],
            raza=data.get('raza', ''),
            edad=data.get('edad'),
            propietario=propietario,
            vivienda=vivienda
        )
        
        return JsonResponse({
            'id': mascota.id,
            'nombre': mascota.nombre,
            'tipo': mascota.tipo,
            'raza': mascota.raza,
            'edad': mascota.edad,
            'propietario_id': mascota.propietario.id,
            'propietario_nombre': f"{mascota.propietario.nombres} {mascota.propietario.apellidos}",
            'vivienda_id': mascota.vivienda.id,
            'codigo_vivienda': mascota.vivienda.codigo
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def detalle_mascota(request, pk):
    """Obtener detalles de una mascota específica"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        mascota = get_object_or_404(Mascota.objects.select_related('propietario', 'vivienda'), id=pk)
        
        return JsonResponse({
            'id': mascota.id,
            'nombre': mascota.nombre,
            'tipo': mascota.tipo,
            'raza': mascota.raza,
            'edad': mascota.edad,
            'propietario_id': mascota.propietario.id,
            'propietario_nombre': f"{mascota.propietario.nombres} {mascota.propietario.apellidos}",
            'vivienda_id': mascota.vivienda.id,
            'codigo_vivienda': mascota.vivienda.codigo
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def modificar_mascota(request, pk):
    """Modificar una mascota existente"""
    if request.method not in ["PUT", "PATCH"]:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        mascota = get_object_or_404(Mascota, id=pk)
        data = json.loads(request.body)
        
        # Actualizar campos si están presentes
        if 'nombre' in data:
            mascota.nombre = data['nombre']
            
        if 'tipo' in data:
            mascota.tipo = data['tipo']
            
        if 'raza' in data:
            mascota.raza = data['raza']
            
        if 'edad' in data:
            mascota.edad = data['edad']
            
        if 'propietario_id' in data:
            propietario = get_object_or_404(Persona, id=data['propietario_id'])
            mascota.propietario = propietario
            
        if 'vivienda_id' in data:
            vivienda = get_object_or_404(Vivienda, id=data['vivienda_id'])
            mascota.vivienda = vivienda
        
        mascota.save()
        
        return JsonResponse({
            'id': mascota.id,
            'nombre': mascota.nombre,
            'tipo': mascota.tipo,
            'raza': mascota.raza,
            'edad': mascota.edad,
            'propietario_id': mascota.propietario.id,
            'propietario_nombre': f"{mascota.propietario.nombres} {mascota.propietario.apellidos}",
            'vivienda_id': mascota.vivienda.id,
            'codigo_vivienda': mascota.vivienda.codigo
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def eliminar_mascota(request, pk):
    """Eliminar una mascota"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        mascota = get_object_or_404(Mascota, id=pk)
        mascota.delete()
        
        return JsonResponse({"message": "Mascota eliminada correctamente"})
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ------------------------------
# ASIGNACIÓN DE PARQUEOS
# ------------------------------

@csrf_exempt
def listar_asignaciones_parqueo(request):
    """Listar todas las asignaciones de parqueos con información detallada"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    asignaciones = AsignacionParqueo.objects.select_related('vehiculo', 'parqueo', 'vehiculo__persona', 'vehiculo__vivienda').all().order_by('-fecha_asignacion')
    data = []
    for asignacion in asignaciones:
        data.append({
            'id': asignacion.id,
            'vehiculo_id': asignacion.vehiculo.id,
            'vehiculo_placa': asignacion.vehiculo.placa,
            'vehiculo_modelo': asignacion.vehiculo.modelo,
            'vehiculo_color': asignacion.vehiculo.color,
            'propietario_nombre': f"{asignacion.vehiculo.persona.nombres} {asignacion.vehiculo.persona.apellidos}",
            'vivienda_codigo': asignacion.vehiculo.vivienda.codigo,
            'parqueo_id': asignacion.parqueo.id,
            'parqueo_numero': asignacion.parqueo.numero,
            'parqueo_piso': asignacion.parqueo.piso,
            'fecha_asignacion': asignacion.fecha_asignacion.isoformat() if asignacion.fecha_asignacion else None,
            'activa': asignacion.activa
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear_asignacion_parqueo(request):
    """Crear una nueva asignación de parqueo"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validar campos requeridos
        required_fields = ['vehiculo_id', 'parqueo_id']
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"Campo requerido: {field}"}, status=400)
        
        # Verificar que el vehículo existe
        vehiculo = get_object_or_404(Vehiculo, id=data['vehiculo_id'])
        
        # Verificar que el parqueo existe
        parqueo = get_object_or_404(Parqueo, id=data['parqueo_id'])
        
        # Verificar que el parqueo no esté ocupado
        if parqueo.ocupado:
            return JsonResponse({"error": "El parqueo ya está ocupado"}, status=400)
        
        # Verificar que el vehículo no tenga ya un parqueo asignado
        asignacion_existente = AsignacionParqueo.objects.filter(vehiculo=vehiculo, activa=True).first()
        if asignacion_existente:
            return JsonResponse({"error": "El vehículo ya tiene un parqueo asignado"}, status=400)
        
        # Crear la asignación
        asignacion = AsignacionParqueo.objects.create(
            vehiculo=vehiculo,
            parqueo=parqueo,
            fecha_asignacion=timezone.now(),
            activa=True
        )
        
        # Marcar el parqueo como ocupado
        parqueo.ocupado = True
        parqueo.save()
        
        return JsonResponse({
            'id': asignacion.id,
            'vehiculo_id': asignacion.vehiculo.id,
            'vehiculo_placa': asignacion.vehiculo.placa,
            'vehiculo_modelo': asignacion.vehiculo.modelo,
            'vehiculo_color': asignacion.vehiculo.color,
            'propietario_nombre': f"{asignacion.vehiculo.persona.nombres} {asignacion.vehiculo.persona.apellidos}",
            'vivienda_codigo': asignacion.vehiculo.vivienda.codigo,
            'parqueo_id': asignacion.parqueo.id,
            'parqueo_numero': asignacion.parqueo.numero,
            'parqueo_piso': asignacion.parqueo.piso,
            'fecha_asignacion': asignacion.fecha_asignacion.isoformat(),
            'activa': asignacion.activa
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def detalle_asignacion_parqueo(request, pk):
    """Obtener detalles de una asignación específica"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        asignacion = get_object_or_404(AsignacionParqueo.objects.select_related('vehiculo', 'parqueo', 'vehiculo__persona', 'vehiculo__vivienda'), id=pk)
        
        return JsonResponse({
            'id': asignacion.id,
            'vehiculo_id': asignacion.vehiculo.id,
            'vehiculo_placa': asignacion.vehiculo.placa,
            'vehiculo_modelo': asignacion.vehiculo.modelo,
            'vehiculo_color': asignacion.vehiculo.color,
            'propietario_nombre': f"{asignacion.vehiculo.persona.nombres} {asignacion.vehiculo.persona.apellidos}",
            'vivienda_codigo': asignacion.vehiculo.vivienda.codigo,
            'parqueo_id': asignacion.parqueo.id,
            'parqueo_numero': asignacion.parqueo.numero,
            'parqueo_piso': asignacion.parqueo.piso,
            'fecha_asignacion': asignacion.fecha_asignacion.isoformat() if asignacion.fecha_asignacion else None,
            'activa': asignacion.activa
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def modificar_asignacion_parqueo(request, pk):
    """Modificar una asignación existente"""
    if request.method not in ["PUT", "PATCH"]:
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        asignacion = get_object_or_404(AsignacionParqueo, id=pk)
        data = json.loads(request.body)
        
        # Si se cambia el parqueo
        if 'parqueo_id' in data:
            nuevo_parqueo = get_object_or_404(Parqueo, id=data['parqueo_id'])
            
            # Liberar el parqueo actual
            parqueo_actual = asignacion.parqueo
            parqueo_actual.ocupado = False
            parqueo_actual.save()
            
            # Verificar que el nuevo parqueo esté disponible
            if nuevo_parqueo.ocupado:
                return JsonResponse({"error": "El nuevo parqueo ya está ocupado"}, status=400)
            
            # Asignar el nuevo parqueo
            asignacion.parqueo = nuevo_parqueo
            nuevo_parqueo.ocupado = True
            nuevo_parqueo.save()
        
        # Actualizar estado activo
        if 'activa' in data:
            asignacion.activa = data['activa']
            
            # Si se desactiva, liberar el parqueo
            if not data['activa']:
                asignacion.parqueo.ocupado = False
                asignacion.parqueo.save()
        
        asignacion.save()
        
        return JsonResponse({
            'id': asignacion.id,
            'vehiculo_id': asignacion.vehiculo.id,
            'vehiculo_placa': asignacion.vehiculo.placa,
            'vehiculo_modelo': asignacion.vehiculo.modelo,
            'vehiculo_color': asignacion.vehiculo.color,
            'propietario_nombre': f"{asignacion.vehiculo.persona.nombres} {asignacion.vehiculo.persona.apellidos}",
            'vivienda_codigo': asignacion.vehiculo.vivienda.codigo,
            'parqueo_id': asignacion.parqueo.id,
            'parqueo_numero': asignacion.parqueo.numero,
            'parqueo_piso': asignacion.parqueo.piso,
            'fecha_asignacion': asignacion.fecha_asignacion.isoformat() if asignacion.fecha_asignacion else None,
            'activa': asignacion.activa
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def eliminar_asignacion_parqueo(request, pk):
    """Eliminar una asignación de parqueo"""
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        asignacion = get_object_or_404(AsignacionParqueo, id=pk)
        
        # Liberar el parqueo
        parqueo = asignacion.parqueo
        parqueo.ocupado = False
        parqueo.save()
        
        # Eliminar la asignación
        asignacion.delete()
        
        return JsonResponse({"message": "Asignación eliminada correctamente"})
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def parqueos_disponibles(request):
    """Obtener lista de parqueos disponibles"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    parqueos = Parqueo.objects.filter(ocupado=False).order_by('piso', 'numero')
    data = []
    for parqueo in parqueos:
        data.append({
            'id': parqueo.id,
            'numero': parqueo.numero,
            'piso': parqueo.piso,
            'tipo': parqueo.tipo
        })
    return JsonResponse(data, safe=False)

# ------------------------------
# REPORTES Y ANÁLISIS
# ------------------------------

@csrf_exempt
def reporte_resumen_general(request):
    """Reporte resumen general del condominio"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        # Estadísticas generales
        total_residentes = Persona.objects.count()
        total_viviendas = Vivienda.objects.count()
        total_parqueos = Parqueo.objects.count()
        parqueos_ocupados = Parqueo.objects.filter(ocupado=True).count()
        total_vehiculos = Vehiculo.objects.count()
        total_mascotas = Mascota.objects.count()
        total_visitantes = Visitante.objects.count()
        
        # Expensas
        total_expensas = Expensa.objects.count()
        expensas_pendientes = Expensa.objects.filter(estado='PENDIENTE').count()
        expensas_pagadas = Expensa.objects.filter(estado='PAGADA').count()
        
        # Multas
        total_multas = Multa.objects.count()
        multas_pendientes = Multa.objects.filter(estado='PENDIENTE').count()
        multas_pagadas = Multa.objects.filter(estado='PAGADA').count()
        
        # Visitas del mes actual
        from datetime import datetime, timedelta
        inicio_mes = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        visitas_mes = Visita.objects.filter(entrada__gte=inicio_mes).count()
        
        return JsonResponse({
            'resumen_general': {
                'residentes': total_residentes,
                'viviendas': total_viviendas,
                'parqueos': {
                    'total': total_parqueos,
                    'ocupados': parqueos_ocupados,
                    'disponibles': total_parqueos - parqueos_ocupados,
                    'porcentaje_ocupacion': round((parqueos_ocupados / total_parqueos * 100) if total_parqueos > 0 else 0, 2)
                },
                'vehiculos': total_vehiculos,
                'mascotas': total_mascotas,
                'visitantes': total_visitantes,
                'visitas_mes_actual': visitas_mes
            },
            'expensas': {
                'total': total_expensas,
                'pendientes': expensas_pendientes,
                'pagadas': expensas_pagadas,
                'porcentaje_pago': round((expensas_pagadas / total_expensas * 100) if total_expensas > 0 else 0, 2)
            },
            'multas': {
                'total': total_multas,
                'pendientes': multas_pendientes,
                'pagadas': multas_pagadas,
                'porcentaje_pago': round((multas_pagadas / total_multas * 100) if total_multas > 0 else 0, 2)
            }
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def reporte_expensas(request):
    """Reporte detallado de expensas"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        # Obtener parámetros de filtro
        mes = request.GET.get('mes')
        año = request.GET.get('año')
        estado = request.GET.get('estado')
        
        # Filtrar expensas
        expensas = Expensa.objects.all()
        
        if mes and año:
            try:
                expensas = expensas.filter(fecha_vencimiento__year=int(año), fecha_vencimiento__month=int(mes))
            except (ValueError, TypeError):
                pass  # Si los valores no son válidos, no aplicar filtro
        elif año:
            try:
                expensas = expensas.filter(fecha_vencimiento__year=int(año))
            except (ValueError, TypeError):
                pass  # Si el año no es válido, no aplicar filtro
            
        if estado:
            expensas = expensas.filter(estado=estado)
        
        # Estadísticas
        total_monto = sum(exp.monto for exp in expensas)
        monto_pagado = sum(exp.monto for exp in expensas.filter(estado='PAGADA'))
        monto_pendiente = sum(exp.monto for exp in expensas.filter(estado='PENDIENTE'))
        
        # Por vivienda
        expensas_por_vivienda = {}
        for exp in expensas:
            codigo = exp.vivienda.codigo
            if codigo not in expensas_por_vivienda:
                expensas_por_vivienda[codigo] = {'total': 0, 'pagado': 0, 'pendiente': 0}
            expensas_por_vivienda[codigo]['total'] += exp.monto
            if exp.estado == 'PAGADA':
                expensas_por_vivienda[codigo]['pagado'] += exp.monto
            else:
                expensas_por_vivienda[codigo]['pendiente'] += exp.monto
        
        return JsonResponse({
            'resumen': {
                'total_monto': total_monto,
                'monto_pagado': monto_pagado,
                'monto_pendiente': monto_pendiente,
                'porcentaje_pago': round((monto_pagado / total_monto * 100) if total_monto > 0 else 0, 2)
            },
            'por_vivienda': expensas_por_vivienda,
            'filtros_aplicados': {
                'mes': mes,
                'año': año,
                'estado': estado
            }
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def reporte_visitas(request):
    """Reporte de visitas y visitantes"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        # Obtener parámetros de filtro
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        
        # Filtrar visitas
        visitas = Visita.objects.all()
        
        if fecha_inicio:
            visitas = visitas.filter(entrada__date__gte=fecha_inicio)
        if fecha_fin:
            visitas = visitas.filter(entrada__date__lte=fecha_fin)
        
        # Estadísticas
        total_visitas = visitas.count()
        visitas_activas = visitas.filter(salida__isnull=True).count()
        visitas_completadas = visitas.filter(salida__isnull=False).count()
        
        # Por vivienda
        visitas_por_vivienda = {}
        for visita in visitas:
            codigo = visita.vivienda_destino.codigo
            if codigo not in visitas_por_vivienda:
                visitas_por_vivienda[codigo] = 0
            visitas_por_vivienda[codigo] += 1
        
        # Visitantes más frecuentes
        visitantes_frecuentes = {}
        for visita in visitas:
            nombre = f"{visita.visitante.nombres} {visita.visitante.apellidos}"
            if nombre not in visitantes_frecuentes:
                visitantes_frecuentes[nombre] = 0
            visitantes_frecuentes[nombre] += 1
        
        return JsonResponse({
            'resumen': {
                'total_visitas': total_visitas,
                'visitas_activas': visitas_activas,
                'visitas_completadas': visitas_completadas
            },
            'por_vivienda': visitas_por_vivienda,
            'visitantes_frecuentes': dict(sorted(visitantes_frecuentes.items(), key=lambda x: x[1], reverse=True)[:10]),
            'filtros_aplicados': {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            }
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def reporte_vehiculos(request):
    """Reporte de vehículos y asignaciones"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        # Estadísticas de vehículos
        total_vehiculos = Vehiculo.objects.count()
        vehiculos_con_parqueo = AsignacionParqueo.objects.filter(activa=True).count()
        vehiculos_sin_parqueo = total_vehiculos - vehiculos_con_parqueo
        
        # Por tipo de vehículo
        tipos_vehiculo = {}
        for vehiculo in Vehiculo.objects.all():
            tipo = vehiculo.tipo.nombre
            if tipo not in tipos_vehiculo:
                tipos_vehiculo[tipo] = 0
            tipos_vehiculo[tipo] += 1
        
        # Asignaciones por piso
        asignaciones_por_piso = {}
        for asignacion in AsignacionParqueo.objects.filter(activa=True):
            piso = asignacion.parqueo.piso
            if piso not in asignaciones_por_piso:
                asignaciones_por_piso[piso] = 0
            asignaciones_por_piso[piso] += 1
        
        return JsonResponse({
            'resumen': {
                'total_vehiculos': total_vehiculos,
                'con_parqueo': vehiculos_con_parqueo,
                'sin_parqueo': vehiculos_sin_parqueo,
                'porcentaje_asignacion': round((vehiculos_con_parqueo / total_vehiculos * 100) if total_vehiculos > 0 else 0, 2)
            },
            'por_tipo': tipos_vehiculo,
            'asignaciones_por_piso': asignaciones_por_piso
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def reporte_ocupacion_parqueos(request):
    """Reporte de ocupación de parqueos"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        # Estadísticas de parqueos
        total_parqueos = Parqueo.objects.count()
        parqueos_ocupados = Parqueo.objects.filter(ocupado=True).count()
        parqueos_disponibles = total_parqueos - parqueos_ocupados
        
        # Por piso
        ocupacion_por_piso = {}
        for parqueo in Parqueo.objects.all():
            piso = parqueo.piso
            if piso not in ocupacion_por_piso:
                ocupacion_por_piso[piso] = {'total': 0, 'ocupados': 0, 'disponibles': 0}
            ocupacion_por_piso[piso]['total'] += 1
            if parqueo.ocupado:
                ocupacion_por_piso[piso]['ocupados'] += 1
            else:
                ocupacion_por_piso[piso]['disponibles'] += 1
        
        # Calcular porcentajes por piso
        for piso in ocupacion_por_piso:
            total = ocupacion_por_piso[piso]['total']
            ocupados = ocupacion_por_piso[piso]['ocupados']
            ocupacion_por_piso[piso]['porcentaje_ocupacion'] = round((ocupados / total * 100) if total > 0 else 0, 2)
        
        return JsonResponse({
            'resumen': {
                'total_parqueos': total_parqueos,
                'ocupados': parqueos_ocupados,
                'disponibles': parqueos_disponibles,
                'porcentaje_ocupacion': round((parqueos_ocupados / total_parqueos * 100) if total_parqueos > 0 else 0, 2)
            },
            'por_piso': ocupacion_por_piso
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def estadisticas_mensuales(request):
    """Estadísticas mensuales del condominio"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        from datetime import datetime, timedelta
        from django.db.models import Count, Sum
        
        # Obtener año y mes (por defecto mes actual)
        año = int(request.GET.get('año', datetime.now().year))
        mes = int(request.GET.get('mes', datetime.now().month))
        
        # Rango de fechas del mes
        inicio_mes = datetime(año, mes, 1)
        if mes == 12:
            fin_mes = datetime(año + 1, 1, 1) - timedelta(days=1)
        else:
            fin_mes = datetime(año, mes + 1, 1) - timedelta(days=1)
        
        # Estadísticas del mes
        visitas_mes = Visita.objects.filter(entrada__date__range=[inicio_mes.date(), fin_mes.date()]).count()
        expensas_mes = Expensa.objects.filter(fecha_vencimiento__date__range=[inicio_mes.date(), fin_mes.date()])
        multas_mes = Multa.objects.filter(fecha_emision__date__range=[inicio_mes.date(), fin_mes.date()])
        
        # Comparación con mes anterior
        if mes == 1:
            mes_anterior = 12
            año_anterior = año - 1
        else:
            mes_anterior = mes - 1
            año_anterior = año
        
        inicio_mes_anterior = datetime(año_anterior, mes_anterior, 1)
        if mes_anterior == 12:
            fin_mes_anterior = datetime(año_anterior + 1, 1, 1) - timedelta(days=1)
        else:
            fin_mes_anterior = datetime(año_anterior, mes_anterior + 1, 1) - timedelta(days=1)
        
        visitas_mes_anterior = Visita.objects.filter(entrada__date__range=[inicio_mes_anterior.date(), fin_mes_anterior.date()]).count()
        
        return JsonResponse({
            'periodo': {
                'año': año,
                'mes': mes,
                'nombre_mes': inicio_mes.strftime('%B')
            },
            'estadisticas': {
                'visitas': {
                    'actual': visitas_mes,
                    'anterior': visitas_mes_anterior,
                    'variacion': visitas_mes - visitas_mes_anterior,
                    'porcentaje_variacion': round(((visitas_mes - visitas_mes_anterior) / visitas_mes_anterior * 100) if visitas_mes_anterior > 0 else 0, 2)
                },
                'expensas': {
                    'total': expensas_mes.count(),
                    'monto_total': sum(exp.monto for exp in expensas_mes),
                    'pagadas': expensas_mes.filter(estado='PAGADA').count(),
                    'pendientes': expensas_mes.filter(estado='PENDIENTE').count()
                },
                'multas': {
                    'total': multas_mes.count(),
                    'monto_total': sum(mul.monto for mul in multas_mes),
                    'pagadas': multas_mes.filter(estado='PAGADA').count(),
                    'pendientes': multas_mes.filter(estado='PENDIENTE').count()
                }
            }
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ------------------------------
# SISTEMA DE NOTIFICACIONES
# ------------------------------

@csrf_exempt
def listar_notificaciones(request):
    """Listar todas las notificaciones del sistema"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        # Obtener parámetros de filtro
        tipo = request.GET.get('tipo')
        leida = request.GET.get('leida')
        fecha_desde = request.GET.get('fecha_desde')
        
        # Crear notificaciones automáticas si no existen
        generar_notificaciones_automaticas()
        
        # Filtrar notificaciones
        notificaciones = Notificacion.objects.all().order_by('-fecha_creacion')
        
        if tipo:
            notificaciones = notificaciones.filter(tipo=tipo)
        if leida is not None:
            notificaciones = notificaciones.filter(leida=leida.lower() == 'true')
        if fecha_desde:
            notificaciones = notificaciones.filter(fecha_creacion__date__gte=fecha_desde)
        
        data = []
        for notif in notificaciones:
            data.append({
                'id': notif.id,
                'titulo': notif.titulo,
                'mensaje': notif.mensaje,
                'tipo': notif.tipo,
                'prioridad': notif.prioridad,
                'leida': notif.leida,
                'fecha_creacion': notif.fecha_creacion.isoformat(),
                'fecha_lectura': notif.fecha_lectura.isoformat() if notif.fecha_lectura else None
            })
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def crear_notificacion(request):
    """Crear una nueva notificación"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # Validar campos requeridos
        required_fields = ['titulo', 'mensaje', 'tipo']
        for field in required_fields:
            if field not in data:
                return JsonResponse({"error": f"Campo requerido: {field}"}, status=400)
        
        # Crear la notificación
        notificacion = Notificacion.objects.create(
            titulo=data['titulo'],
            mensaje=data['mensaje'],
            tipo=data['tipo'],
            prioridad=data.get('prioridad', 'MEDIA'),
            leida=False
        )
        
        return JsonResponse({
            'id': notificacion.id,
            'titulo': notificacion.titulo,
            'mensaje': notificacion.mensaje,
            'tipo': notificacion.tipo,
            'prioridad': notificacion.prioridad,
            'leida': notificacion.leida,
            'fecha_creacion': notificacion.fecha_creacion.isoformat(),
            'fecha_lectura': None
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def marcar_notificacion_leida(request, pk):
    """Marcar una notificación como leída"""
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        notificacion = get_object_or_404(Notificacion, id=pk)
        
        if not notificacion.leida:
            notificacion.leida = True
            notificacion.fecha_lectura = timezone.now()
            notificacion.save()
        
        return JsonResponse({
            'id': notificacion.id,
            'titulo': notificacion.titulo,
            'mensaje': notificacion.mensaje,
            'tipo': notificacion.tipo,
            'prioridad': notificacion.prioridad,
            'leida': notificacion.leida,
            'fecha_creacion': notificacion.fecha_creacion.isoformat(),
            'fecha_lectura': notificacion.fecha_lectura.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def alertas_automaticas(request):
    """Generar alertas automáticas del sistema"""
    if request.method != "GET":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    
    try:
        alertas = []
        
        # Verificar expensas vencidas
        from datetime import datetime, timedelta
        hoy = datetime.now().date()
        expensas_vencidas = Expensa.objects.filter(
            estado='PENDIENTE',
            fecha_vencimiento__lt=hoy
        ).count()
        
        if expensas_vencidas > 0:
            alertas.append({
                'tipo': 'EXPENSA_VENCIDA',
                'titulo': f'Expensas Vencidas',
                'mensaje': f'Hay {expensas_vencidas} expensas vencidas que requieren atención',
                'prioridad': 'ALTA',
                'cantidad': expensas_vencidas
            })
        
        # Verificar multas pendientes
        multas_pendientes = Multa.objects.filter(estado='PENDIENTE').count()
        if multas_pendientes > 0:
            alertas.append({
                'tipo': 'MULTA_PENDIENTE',
                'titulo': f'Multas Pendientes',
                'mensaje': f'Hay {multas_pendientes} multas pendientes de pago',
                'prioridad': 'MEDIA',
                'cantidad': multas_pendientes
            })
        
        # Verificar visitas activas
        visitas_activas = Visita.objects.filter(salida__isnull=True).count()
        if visitas_activas > 0:
            alertas.append({
                'tipo': 'VISITA_ACTIVA',
                'titulo': f'Visitas en Curso',
                'mensaje': f'Hay {visitas_activas} visitas activas en el condominio',
                'prioridad': 'BAJA',
                'cantidad': visitas_activas
            })
        
        # Verificar ocupación de parqueos
        total_parqueos = Parqueo.objects.count()
        parqueos_ocupados = Parqueo.objects.filter(ocupado=True).count()
        porcentaje_ocupacion = (parqueos_ocupados / total_parqueos * 100) if total_parqueos > 0 else 0
        
        if porcentaje_ocupacion > 90:
            alertas.append({
                'tipo': 'PARQUEO_ALTO',
                'titulo': f'Alta Ocupación de Parqueos',
                'mensaje': f'La ocupación de parqueos es del {porcentaje_ocupacion:.1f}%',
                'prioridad': 'MEDIA',
                'porcentaje': porcentaje_ocupacion
            })
        
        return JsonResponse({
            'alertas': alertas,
            'total_alertas': len(alertas),
            'fecha_generacion': timezone.now().isoformat()
        })
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def generar_notificaciones_automaticas():
    """Generar notificaciones automáticas basadas en el estado del sistema"""
    try:
        from datetime import datetime, timedelta
        
        # Verificar si ya existen notificaciones recientes (últimas 24 horas)
        hace_24h = timezone.now() - timedelta(hours=24)
        notificaciones_recientes = Notificacion.objects.filter(
            fecha_creacion__gte=hace_24h,
            tipo__in=['EXPENSA_VENCIDA', 'MULTA_PENDIENTE', 'VISITA_ACTIVA', 'PARQUEO_ALTO']
        ).count()
        
        if notificaciones_recientes > 0:
            return  # Ya hay notificaciones recientes
        
        # Generar alertas automáticas
        hoy = datetime.now().date()
        
        # Expensas vencidas
        expensas_vencidas = Expensa.objects.filter(
            estado='PENDIENTE',
            fecha_vencimiento__lt=hoy
        ).count()
        
        if expensas_vencidas > 0:
            Notificacion.objects.get_or_create(
                titulo=f'Expensas Vencidas ({expensas_vencidas})',
                mensaje=f'Hay {expensas_vencidas} expensas vencidas que requieren atención inmediata',
                tipo='EXPENSA_VENCIDA',
                prioridad='ALTA',
                defaults={'leida': False}
            )
        
        # Multas pendientes
        multas_pendientes = Multa.objects.filter(estado='PENDIENTE').count()
        if multas_pendientes > 0:
            Notificacion.objects.get_or_create(
                titulo=f'Multas Pendientes ({multas_pendientes})',
                mensaje=f'Hay {multas_pendientes} multas pendientes de pago',
                tipo='MULTA_PENDIENTE',
                prioridad='MEDIA',
                defaults={'leida': False}
            )
        
        # Visitas activas
        visitas_activas = Visita.objects.filter(salida__isnull=True).count()
        if visitas_activas > 0:
            Notificacion.objects.get_or_create(
                titulo=f'Visitas Activas ({visitas_activas})',
                mensaje=f'Hay {visitas_activas} visitas en curso en el condominio',
                tipo='VISITA_ACTIVA',
                prioridad='BAJA',
                defaults={'leida': False}
            )
        
    except Exception as e:
        print(f"Error generando notificaciones automáticas: {e}")

# ------------------------------
# FUNCIONES GENÉRICAS
# ------------------------------

@csrf_exempt
def listar(request, model_name):
    """
    Listar todos los objetos de un modelo.
    """
    model = globals()[model_name]
    objects = model.objects.all()
    data = [model_to_dict(obj) for obj in objects]
    return JsonResponse(data, safe=False)

@csrf_exempt
def crear(request, model_name):
    """
    Crear un objeto.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    model = globals()[model_name]
    data = json.loads(request.body)
    obj = model.objects.create(**data)
    return JsonResponse(model_to_dict(obj))

@csrf_exempt
def modificar(request, model_name, pk):
    """
    Modificar un objeto.
    """
    if request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    model = globals()[model_name]
    obj = get_object_or_404(model, pk=pk)
    data = json.loads(request.body)
    for key, value in data.items():
        setattr(obj, key, value)
    obj.save()
    return JsonResponse(model_to_dict(obj))

@csrf_exempt
def eliminar(request, model_name, pk):
    """
    Eliminar un objeto.
    """
    if request.method != "DELETE":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    model = globals()[model_name]
    obj = get_object_or_404(model, pk=pk)
    obj.delete()
    return JsonResponse({"status": "ok"})
