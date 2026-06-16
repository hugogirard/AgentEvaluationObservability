param foundryResourceName string
param projectResourceName string
param appInsightResourceName string
param projectPrincipalId string
param mcpServerEndpoint string
param mcpServerSubscriptionKey string

resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: foundryResourceName
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  parent: aiFoundry
  name: projectResourceName
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: appInsightResourceName
}

resource connectionAppInsight 'Microsoft.CognitiveServices/accounts/projects/connections@2026-03-01' = {
  name: '${foundryResourceName}-appinsights'
  parent: project
  properties: {
    category: 'AppInsights'
    target: appInsights.id
    authType: 'ApiKey'
    isSharedToAll: true
    credentials: {
      key: appInsights.properties.ConnectionString
    }
    metadata: {
      ApiType: 'Azure'
      ResourceId: appInsights.id
    }
  }
}

resource connectionMCPServer 'Microsoft.CognitiveServices/accounts/projects/connections@2026-03-01' = {
  name: 'WEALTH-MCP-SERVER'
  parent: project
  properties: {
    authType: 'CustomKeys'
    category: 'RemoteTool'
    target: 'https://${mcpServerEndpoint}/mcp'
    useWorkspaceManagedIdentity: false
    isSharedToAll: false
    sharedUserList: []
    credentials: {
      keys: {
        'x-mcp-server-key': mcpServerSubscriptionKey
      }
    }
    metadata: {
      type: 'custom_MCP'
    }
  }
}

@description('Built-in Role: [Reader]')
resource reader 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'acdd72a7-3385-48ef-bd42-f606fba81ae7'
  scope: subscription()
}

module projectReaderAppInsight 'br/public:avm/ptn/authorization/resource-role-assignment:0.1.2' = {
  name: 'webArcPull'
  params: {
    principalId: projectPrincipalId
    resourceId: appInsights.id
    roleDefinitionId: reader.id
  }
}
