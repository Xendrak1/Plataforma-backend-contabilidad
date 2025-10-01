"""
Script para probar la conexión a la base de datos PostgreSQL en Azure.
"""
import os
import sys
from dotenv import load_dotenv
import psycopg2
from pathlib import Path

# Cargar variables de entorno
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

def test_connection():
    """Prueba la conexión a la base de datos PostgreSQL en Azure."""
    try:
        print("🔄 Intentando conectar a la base de datos Azure PostgreSQL...")
        print(f"   Host: {os.getenv('DB_HOST')}")
        print(f"   Puerto: {os.getenv('DB_PORT')}")
        print(f"   Base de datos: {os.getenv('DB_NAME')}")
        print(f"   Usuario: {os.getenv('DB_USER')}")
        print()
        
        # Intentar conexión
        connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            sslmode='require'  # Azure PostgreSQL requiere SSL
        )
        
        # Crear un cursor y ejecutar una consulta simple
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        db_version = cursor.fetchone()
        
        print("✅ ¡Conexión exitosa!")
        print(f"   Versión de PostgreSQL: {db_version[0]}")
        
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al conectar a la base de datos:")
        print(f"   {type(e).__name__}: {e}")
        return False

if __name__ == '__main__':
    success = test_connection()
    sys.exit(0 if success else 1)
