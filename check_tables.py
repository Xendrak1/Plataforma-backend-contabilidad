#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONDOMINIO.settings')
django.setup()

from django.db import connection

def check_all_tables():
    """Verificar todas las tablas en la base de datos"""
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
            
            print("=" * 60)
            print("📊 TABLAS DISPONIBLES EN LA BASE DE DATOS")
            print("=" * 60)
            
            for i, (schema, table_name) in enumerate(tables, 1):
                print(f"{i:2d}. {table_name}")
            
            print(f"\n📈 TOTAL: {len(tables)} tablas encontradas")
            print("=" * 60)
            
            # Verificar columnas de algunas tablas importantes
            important_tables = ['personas', 'viviendas', 'residente_vivienda', 'parqueos', 'expensas', 'multas', 'pagos']
            
            print("\n🔍 DETALLES DE TABLAS IMPORTANTES:")
            print("-" * 60)
            
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
                    
                    print(f"\n📋 Tabla: {table}")
                    print(f"   Columnas: {len(columns)}")
                    for col_name, data_type, nullable in columns[:5]:  # Mostrar solo las primeras 5
                        print(f"   - {col_name} ({data_type}) {'NULL' if nullable == 'YES' else 'NOT NULL'}")
                    if len(columns) > 5:
                        print(f"   ... y {len(columns) - 5} columnas más")
                else:
                    print(f"\n❌ Tabla: {table} - NO EXISTE")
                    
        except Exception as e:
            print(f"❌ Error al consultar tablas: {e}")
            # Intentar método alternativo
            try:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                print(f"🔍 Versión de PostgreSQL: {version}")
            except Exception as e2:
                print(f"❌ Error al obtener versión: {e2}")

if __name__ == "__main__":
    try:
        check_all_tables()
    except Exception as e:
        print(f"❌ Error: {e}")
