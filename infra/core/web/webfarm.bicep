param resourceName string
param location string

resource asp 'Microsoft.Web/serverfarms@2024-11-01' = {
  name: resourceName
  location: location
  kind: 'linux'
  properties: {
    reserved: true
  }
  sku: {
    tier: 'PremiumV3'
    name: 'P1V3'
  }
}

output resourceId string = asp.id
