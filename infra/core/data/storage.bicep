param storageResourceName string
param location string
param tags object

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: storageResourceName
  location: location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
  tags: tags
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
    }
    allowSharedKeyAccess: true
  }
}

output blobEndpoint string = storage.properties.primaryEndpoints.blob
