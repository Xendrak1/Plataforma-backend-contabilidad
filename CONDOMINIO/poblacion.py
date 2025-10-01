from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Carga datos de prueba desde SQL"

    def handle(self, *args, **kwargs):
        # Ruta a tu archivo SQL
        ruta_sql = r"C:\xampp\htdocs\MIS PROGRAMAS\CONDOMINIO\CONDOMINIO\CONDOMINIO\poblacion.sql"

        with open(ruta_sql, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        with connection.cursor() as cursor:
            cursor.execute(sql_content)

        self.stdout.write(self.style.SUCCESS("Datos de prueba cargados correctamente"))
