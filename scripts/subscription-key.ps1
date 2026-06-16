$resourceGroup = "rg-fsi-demo-eval"

# Find the MCP app service in the resource group
$appName = az webapp list --resource-group $resourceGroup --query "[?starts_with(name, 'app-mcp-')].name" -o tsv

if (-not $appName) {
    Write-Error "No app service matching 'app-mcp-*' found in resource group '$resourceGroup'"
    exit 1
}

Write-Host "Found App Service: $appName" -ForegroundColor Cyan

# Generate a new GUID as the subscription key
$subscriptionKey = [guid]::NewGuid().ToString()

# Set the MCP_SERVER_KEY app setting on the app service
az webapp config appsettings set `
    --name $appName `
    --resource-group $resourceGroup `
    --settings MCP_SERVER_KEY=$subscriptionKey `
    --output none

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to set app setting on '$appName'"
    exit 1
}

Write-Host ""
Write-Host "MCP_SERVER_KEY has been set on '$appName'" -ForegroundColor Green
Write-Host ""
Write-Host "x-mcp-server-key: $subscriptionKey" -ForegroundColor Yellow