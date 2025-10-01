# Script para configurar variables de entorno en Azure App Service
# Ejecuta estos comandos en Azure Cloud Shell o con Azure CLI instalado

# Variables de configuración
$resourceGroup = "tu-resource-group"  # Cambia esto por tu grupo de recursos
$appName = "contabilidadwebapp-backend"

# Configurar variables de entorno de la base de datos
az webapp config appsettings set --resource-group $resourceGroup --name $appName --settings `
    DB_HOST="condominio-flutter.postgres.database.azure.com" `
    DB_PORT="5432" `
    DB_NAME="Condominio" `
    DB_USER="jeadmin" `
    DB_PASSWORD="ByuSix176488" `
    DJANGO_DEBUG="False" `
    WEBSITE_HOSTNAME="contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net"

Write-Host "✅ Variables de entorno configuradas exitosamente"
Write-Host "🔄 Reiniciando la aplicación..."

# Reiniciar la aplicación para aplicar los cambios
az webapp restart --resource-group $resourceGroup --name $appName

Write-Host "✅ Aplicación reiniciada"
Write-Host "🌐 URL: https://contabilidadwebapp-backend-dnhmfyfda0ehb9f7.brazilsouth-01.azurewebsites.net"
