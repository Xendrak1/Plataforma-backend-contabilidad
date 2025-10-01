# Configuración de Base de Datos Azure PostgreSQL

## 📋 Información de la Base de Datos

La aplicación está configurada para conectarse a una base de datos PostgreSQL en Azure con las siguientes características:

- **Servidor**: condominio-flutter.postgres.database.azure.com
- **Puerto**: 5432
- **Base de datos**: Condominio
- **Usuario**: jeadmin
- **SSL**: Requerido (configurado automáticamente)

## 🔧 Configuración

### 1. Variables de Entorno

El proyecto utiliza variables de entorno para gestionar las credenciales de forma segura. Estas se cargan desde el archivo `.env`.

#### Archivo `.env` (ya creado)
Este archivo contiene las credenciales reales y **NO** debe subirse a Git (ya está en `.gitignore`):

```env
DB_HOST=condominio-flutter.postgres.database.azure.com
DB_PORT=5432
DB_NAME=Condominio
DB_USER=jeadmin
DB_PASSWORD=ByuSix176488
DJANGO_DEBUG=False
```

#### Archivo `.env.example` (plantilla)
Este archivo es una plantilla que sí se puede subir a Git:

```env
DB_HOST=tu-servidor.postgres.database.azure.com
DB_PORT=5432
DB_NAME=nombre-base-datos
DB_USER=usuario
DB_PASSWORD=contraseña
DJANGO_DEBUG=False
```

### 2. Dependencias

Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

Las dependencias principales incluyen:
- `Django==5.2`
- `psycopg2-binary==2.9.9` (adaptador PostgreSQL)
- `python-dotenv==1.0.0` (carga variables de entorno)
- `django-cors-headers==4.4.0`
- `gunicorn==21.2.0`
- `whitenoise==6.7.0`

### 3. Configuración de Django

El archivo `settings.py` está configurado para:
- Cargar automáticamente las variables de entorno desde `.env`
- Conectarse a PostgreSQL en Azure con SSL
- Usar valores por defecto si no se encuentran las variables

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'Condominio'),
        'USER': os.environ.get('DB_USER', 'jeadmin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'ByuSix176488'),
        'HOST': os.environ.get('DB_HOST', 'condominio-flutter.postgres.database.azure.com'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',  # Azure PostgreSQL requiere SSL
        }
    }
}
```

## 🧪 Probar la Conexión

Ejecuta el script de prueba para verificar la conexión:

```bash
python test_db_connection.py
```

Si la conexión es exitosa, verás:
```
✅ ¡Conexión exitosa!
   Versión de PostgreSQL: PostgreSQL 17.5...
```

## 🚀 Migraciones

### Aplicar migraciones a la base de datos de Azure

```bash
python manage.py migrate
```

### Crear un superusuario (admin)

```bash
python manage.py createsuperuser
```

### Verificar las tablas creadas

Puedes verificar las tablas con el comando personalizado:

```bash
python manage.py check_tables
```

## 📊 Acceso a la Base de Datos

### Desde pgAdmin o herramientas similares:

- **Host**: condominio-flutter.postgres.database.azure.com
- **Puerto**: 5432
- **Base de datos**: Condominio
- **Usuario**: jeadmin
- **Password**: ByuSix176488
- **SSL Mode**: Require

### Desde código Python:

```python
import psycopg2

connection = psycopg2.connect(
    host='condominio-flutter.postgres.database.azure.com',
    port='5432',
    database='Condominio',
    user='jeadmin',
    password='ByuSix176488',
    sslmode='require'
)
```

## 🔒 Seguridad

### Buenas prácticas implementadas:

1. ✅ Credenciales en archivo `.env` (no en el código)
2. ✅ Archivo `.env` excluido de Git mediante `.gitignore`
3. ✅ SSL habilitado para la conexión a Azure
4. ✅ Variables de entorno con valores por defecto
5. ✅ Archivo `.env.example` como plantilla para otros desarrolladores

### Recomendaciones adicionales:

- 🔐 Cambia la contraseña periódicamente
- 🔐 Usa Azure Key Vault para producción
- 🔐 Habilita firewall en Azure PostgreSQL
- 🔐 Revisa los logs de acceso regularmente

## 🌐 Despliegue en Azure

### Variables de entorno en Azure App Service:

En el portal de Azure, configura las variables de entorno en:
**Configuration → Application settings**

```
DB_HOST = condominio-flutter.postgres.database.azure.com
DB_PORT = 5432
DB_NAME = Condominio
DB_USER = jeadmin
DB_PASSWORD = ByuSix176488
DJANGO_DEBUG = False
```

## 📝 Comandos Útiles

```bash
# Ejecutar el servidor de desarrollo
python manage.py runserver

# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Acceder al shell de Django
python manage.py shell

# Verificar configuración
python manage.py check

# Recolectar archivos estáticos
python manage.py collectstatic
```

## ❓ Troubleshooting

### Error: "connection refused"
- Verifica que el firewall de Azure permita tu IP
- Confirma que las credenciales sean correctas

### Error: "SSL required"
- Asegúrate de que `'sslmode': 'require'` esté en OPTIONS

### Error: "no such table"
- Ejecuta las migraciones: `python manage.py migrate`

### Error: "could not resolve dotenv"
- Instala la dependencia: `pip install python-dotenv`

## 📚 Recursos

- [Django Database Settings](https://docs.djangoproject.com/en/5.2/ref/settings/#databases)
- [Azure Database for PostgreSQL](https://learn.microsoft.com/azure/postgresql/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
