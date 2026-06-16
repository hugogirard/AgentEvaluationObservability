$resourceGroup = "rg-fsi-demo-eval"

# Find the MCP app service in the resource group
$appName = az webapp list --resource-group $resourceGroup --query "[?starts_with(name, 'app-mcp-')].name" -o tsv

if (-not $appName) {
    Write-Error "No app service matching 'app-mcp-*' found in resource group '$resourceGroup'"
    exit 1
}

Write-Host "Found App Service: $appName" -ForegroundColor Cyan

# Retrieve the MCP_SERVER_KEY app setting
$subscriptionKey = az webapp config appsettings list `
    --name $appName `
    --resource-group $resourceGroup `
    --query "[?name=='MCP_SERVER_KEY'].value" -o tsv

if (-not $subscriptionKey) {
    Write-Error "MCP_SERVER_KEY not found on '$appName'"
    exit 1
}

Write-Host ""
Write-Host "MCP_SERVER_KEY retrieved from '$appName'" -ForegroundColor Green
Write-Host ""
Write-Host "x-mcp-server-key: $subscriptionKey" -ForegroundColor Yellow