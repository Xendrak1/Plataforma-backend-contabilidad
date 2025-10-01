from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Verificar todas las tablas en la base de datos'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                # Obtener todas las tablas - consulta compatible con PostgreSQL 17
                cursor.execute("""
                    SELECT schemaname, tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                    ORDER BY tablename;
                """)
                
                tables = cursor.fetchall()
                
                self.stdout.write("=" * 60)
                self.stdout.write(self.style.SUCCESS("📊 TABLAS DISPONIBLES EN LA BASE DE DATOS"))
                self.stdout.write("=" * 60)
                
                for i, (schema, table_name) in enumerate(tables, 1):
                    self.stdout.write(f"{i:2d}. {table_name}")
                
                self.stdout.write(f"\n📈 TOTAL: {len(tables)} tablas encontradas")
                self.stdout.write("=" * 60)
                
                # Verificar columnas de algunas tablas importantes
                important_tables = [
                    'personas', 'viviendas', 'residente_vivienda', 'parqueos', 
                    'expensas', 'multas', 'pagos', 'visitantes', 'visitas',
                    'areas_comunes', 'reservas', 'comunicados', 'vehiculos',
                    'mascotas', 'tipos_vehiculo', 'tipos_infraccion'
                ]
                
                self.stdout.write("\n🔍 DETALLES DE TABLAS IMPORTANTES:")
                self.stdout.write("-" * 60)
                
                for table in important_tables:
                    # Verificar si la tabla existe
                    cursor.execute("""
                        SELECT EXISTS (
                            SELECT 1 FROM information_schema.tables 
                            WHERE table_name = %s AND table_schema = 'public'
                        );
                    """, [table])
                    
                    exists = cursor.fetchone()[0]
                    
                    if exists:
                        cursor.execute("""
                            SELECT column_name, data_type, is_nullable
                            FROM information_schema.columns 
                            WHERE table_name = %s AND table_schema = 'public'
                            ORDER BY ordinal_position;
                        """, [table])
                        columns = cursor.fetchall()
                        
                        self.stdout.write(f"\n📋 Tabla: {table}")
                        self.stdout.write(f"   Columnas: {len(columns)}")
                        for col_name, data_type, nullable in columns[:5]:  # Mostrar solo las primeras 5
                            self.stdout.write(f"   - {col_name} ({data_type}) {'NULL' if nullable == 'YES' else 'NOT NULL'}")
                        if len(columns) > 5:
                            self.stdout.write(f"   ... y {len(columns) - 5} columnas más")
                    else:
                        self.stdout.write(f"\n❌ Tabla: {table} - NO EXISTE")
                        
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error al consultar tablas: {e}"))
                # Intentar método alternativo
                try:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()[0]
                    self.stdout.write(f"🔍 Versión de PostgreSQL: {version}")
                except Exception as e2:
                    self.stdout.write(self.style.ERROR(f"❌ Error al obtener versión: {e2}"))
