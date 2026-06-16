param resourceName string
param location string
param tags object

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2025-11-01-preview' = {
  name: resourceName
  tags: tags
  kind: 'GlobalDocumentDB'
  location: location
  properties: {
    capacity: {
      totalThroughputLimit: 1000
    }
    databaseAccountOfferType: 'Standard'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    disableLocalAuth: false
    enableAutomaticFailover: false
    enableMultipleWriteLocations: false
    publicNetworkAccess: 'Enabled'
    enableFreeTier: false
  }

  resource database 'sqlDatabases@2025-11-01-preview' = {
    name: 'contoso'
    properties: {
      resource: {
        id: 'contoso'
      }
    }
    resource clientContainer 'containers@2025-11-01-preview' = {
      name: 'client'
      properties: {
        resource: {
          id: 'client'
          partitionKey: {
            kind: 'Hash'
            paths: [
              '/clientId'
            ]
          }
        }
      }
    }
    resource fundContainer 'containers@2025-11-01-preview' = {
      name: 'fund'
      properties: {
        resource: {
          id: 'fund'
          partitionKey: {
            kind: 'Hash'
            paths: [
              '/fundCode'
            ]
          }
        }
      }
    }
  }
}

output resourceName string = cosmos.name
output endpoint string = 'https://${cosmos.properties.documentEndpoint}'
