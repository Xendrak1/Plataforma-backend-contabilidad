#!/bin/bash
# Script para configurar variables de entorno en Azure App Service
# Ejecuta este script en Azure Cloud Shell o con Azure CLI instalado

# Variables de configuración
RESOURCE_GROUP="tu-resource-group"  # Cambia esto por tu grupo de recursos
APP_NAME="contabilidadwebapp-backend"

echo "🔧 Configurando variables de entorno en Azure App Service..."

# Configurar variables de entorno de la base de datos
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --settings \
        DB_HOST="condominio-flutter.postgres.database.azure.com" \
        DB_PORT="5432" \
        DB_NAME="Condominio" \
        DB_USER="jeadmin" \
        DB_PASSWORD="ByuSix176488" \
        DJANGO_DEBUG="False" \
        WEBSITE_HOSTNAME="contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net"

echo "✅ Variables de entorno configuradas exitosamente"
echo "🔄 Reiniciando la aplicación..."

# Reiniciar la aplicación para aplicar los cambios
az webapp restart --resource-group $RESOURCE_GROUP --name $APP_NAME

echo "✅ Aplicación reiniciada"
echo "🌐 URL: https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net"
