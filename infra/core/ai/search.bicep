param aiSearchResourceName string
param location string
param tags object

resource agentAiSearch 'Microsoft.Search/searchServices@2026-03-01-preview' = {
  name: aiSearchResourceName
  location: location
  tags: tags
  sku: {
    name: 'basic' // Should be higher for none dev workload
  }
  properties: {
    disableLocalAuth: false
    authOptions: {
      aadOrApiKey: {
        aadAuthFailureMode: 'http401WithBearerChallenge'
      }
    }
    partitionCount: 1 // Can be changed based on volume
    replicaCount: 1 // No SLA shouldn't be used for production
    publicNetworkAccess: 'Enabled'
    semanticSearch: 'disabled'
  }
}
