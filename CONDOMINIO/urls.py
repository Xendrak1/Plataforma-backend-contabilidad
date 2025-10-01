from django.urls import path, include
from django.http import JsonResponse

def api_info(request):
    return JsonResponse({
        'message': 'API del Sistema de Condominio',
        'version': '1.0.0',
        'endpoints': {
            'residentes': '/api/residentes/',
            'viviendas': '/api/viviendas/',
            'parqueos': '/api/parqueos/',
            'visitantes': '/api/visitantes/',
            'reservas': '/api/reservas/',
            'areas': '/api/areas/',
            'expensas': '/api/expensas/',
            'pagos': '/api/pagos/',
            'multas': '/api/multas/',
            'comunicados': '/api/comunicados/',
            'dashboard': '/api/dashboard/'
        }
    })

urlpatterns = [
    # Página de información de la API
    path('', api_info, name='api_info'),
    # API endpoints con prefijo /api/
    path('api/', include('CONDOMINIO.api_urls')),
]
