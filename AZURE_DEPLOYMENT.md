# Guía para configurar variables de entorno en Azure App Service

## 📋 **Información del Backend**

- **Nombre de la App**: contabilidadwebapp-backend
- **URL**: https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net
- **Región**: Brazil South

## 🎯 **Paso 1: Verificar el despliegue**

1. Ve a GitHub Actions: https://github.com/Xendrak1/Plataforma-backend-contabilidad/actions
2. Verifica que el workflow se haya ejecutado correctamente
3. Espera a que termine (toma unos 3-5 minutos)

## ⚙️ **Paso 2: Configurar variables de entorno**

### **Opción A: Portal de Azure (Más fácil)** ⭐

1. Inicia sesión en: https://portal.azure.com
2. Busca tu App Service: `contabilidadwebapp-backend`
3. En el menú izquierdo, ve a: **Settings → Configuration**
4. En la pestaña **"Application settings"**, haz clic en **"+ New application setting"**
5. Agrega cada variable una por una:

   | Nombre | Valor |
   |--------|-------|
   | `DB_HOST` | `condominio-flutter.postgres.database.azure.com` |
   | `DB_PORT` | `5432` |
   | `DB_NAME` | `Condominio` |
   | `DB_USER` | `jeadmin` |
   | `DB_PASSWORD` | `ByuSix176488` |
   | `DJANGO_DEBUG` | `False` |

6. Haz clic en **"Save"** (arriba)
7. Haz clic en **"Continue"** cuando pregunte si quieres reiniciar

### **Opción B: Azure CLI**

Si tienes Azure CLI instalado, ejecuta uno de estos scripts:

**Windows PowerShell:**
```powershell
.\configure_azure_env.ps1
```

**Linux/Mac/Git Bash:**
```bash
bash configure_azure_env.sh
```

**Nota:** Antes de ejecutar, cambia `tu-resource-group` por el nombre real de tu grupo de recursos en Azure.

### **Opción C: Azure Cloud Shell**

1. Abre: https://shell.azure.com
2. Copia y pega estos comandos (cambia `TU_RESOURCE_GROUP`):

```bash
RESOURCE_GROUP="TU_RESOURCE_GROUP"  # ⚠️ Cambia esto
APP_NAME="contabilidadwebapp-backend"

az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --settings \
        DB_HOST="condominio-flutter.postgres.database.azure.com" \
        DB_PORT="5432" \
        DB_NAME="Condominio" \
        DB_USER="jeadmin" \
        DB_PASSWORD="ByuSix176488" \
        DJANGO_DEBUG="False"

az webapp restart --resource-group $RESOURCE_GROUP --name $APP_NAME
```

## 🔍 **Paso 3: Verificar que funcione**

### **Prueba 1: Verificar que el sitio esté activo**
Abre en tu navegador:
```
https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net
```

Deberías ver la página por defecto de Django o tu aplicación.

### **Prueba 2: Verificar el admin de Django**
```
https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net/admin
```

### **Prueba 3: Ver logs en tiempo real**

En el portal de Azure:
1. Ve a tu App Service
2. En el menú izquierdo: **Monitoring → Log stream**
3. Verás los logs en tiempo real

O con CLI:
```bash
az webapp log tail --resource-group TU_RESOURCE_GROUP --name contabilidadwebapp-backend
```

## 🚀 **Paso 4: Ejecutar migraciones en Azure**

Necesitas ejecutar las migraciones en la base de datos de Azure. Puedes hacerlo de dos formas:

### **Opción A: SSH a Azure App Service**

1. En el portal de Azure, ve a tu App Service
2. En el menú izquierdo: **Development Tools → SSH**
3. Haz clic en **"Go"**
4. Ejecuta:
   ```bash
   cd /home/site/wwwroot
   python manage.py migrate
   python manage.py createsuperuser
   ```

### **Opción B: Desde tu computadora con Azure CLI**

```bash
az webapp ssh --resource-group TU_RESOURCE_GROUP --name contabilidadwebapp-backend
cd /home/site/wwwroot
python manage.py migrate
```

## 📊 **Comandos útiles de Azure CLI**

```bash
# Ver información de la app
az webapp show --resource-group TU_RESOURCE_GROUP --name contabilidadwebapp-backend

# Ver configuración actual
az webapp config appsettings list --resource-group TU_RESOURCE_GROUP --name contabilidadwebapp-backend

# Ver logs
az webapp log tail --resource-group TU_RESOURCE_GROUP --name contabilidadwebapp-backend

# Reiniciar app
az webapp restart --resource-group TU_RESOURCE_GROUP --name contabilidadwebapp-backend

# Ver estado del despliegue
az webapp deployment list-publishing-profiles --resource-group TU_RESOURCE_GROUP --name contabilidadwebapp-backend
```

## 🔒 **Configurar firewall de PostgreSQL**

Para que Azure pueda conectarse a tu base de datos PostgreSQL:

1. Ve al portal de Azure
2. Busca tu servidor PostgreSQL: `condominio-flutter`
3. Ve a: **Settings → Networking**
4. En **Firewall rules**, agrega:
   - **Rule name**: `AllowAzureServices`
   - **Start IP**: `0.0.0.0`
   - **End IP**: `0.0.0.0`
   
   O marca: ☑️ **"Allow public access from any Azure service within Azure to this server"**

5. Haz clic en **"Save"**

## ❓ **Troubleshooting**

### Error: "Resource group not found"
- Encuentra tu resource group con: `az group list --output table`

### Error: "Connection refused" en la BD
- Verifica el firewall de PostgreSQL (ver arriba)
- Verifica que las variables de entorno estén configuradas

### La app muestra error 500
- Ve a los logs en Azure Portal
- Verifica que las migraciones se hayan ejecutado
- Verifica que las variables de entorno estén correctas

### ¿Cómo encontrar mi Resource Group?

**Opción 1: Azure Portal**
1. Ve a: https://portal.azure.com
2. Busca tu App Service: `contabilidadwebapp-backend`
3. En la página principal verás: **Resource group: NOMBRE_AQUI**

**Opción 2: Azure CLI**
```bash
az webapp list --query "[?name=='contabilidadwebapp-backend'].resourceGroup" -o tsv
```

## 📚 **Recursos adicionales**

- [Configuración de App Service](https://learn.microsoft.com/azure/app-service/configure-common)
- [Despliegue continuo con GitHub Actions](https://learn.microsoft.com/azure/app-service/deploy-github-actions)
- [Azure Database for PostgreSQL](https://learn.microsoft.com/azure/postgresql/)
