param resourceName string
param location string
param tags object

resource acr 'Microsoft.ContainerRegistry/registries@2025-11-01' = {
  name: resourceName
  location: location
  tags: tags
  sku: {
    name: 'Standard'
  }
  properties: {
    adminUserEnabled: true
    publicNetworkAccess: 'Enabled'
  }
}

output resourceId string = acr.id
output resourceName string = replace(acr.name, '.azurecr.io', '')
