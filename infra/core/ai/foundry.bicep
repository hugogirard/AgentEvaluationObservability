param accountName string
param location string
param appInsightResourceName string
param tags object

resource insights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: appInsightResourceName
}

#disable-next-line BCP036
resource account 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' = {
  name: accountName
  location: location
  tags: tags
  sku: {
    name: 'S0'
  }
  kind: 'AIServices'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    allowProjectManagement: true
    customSubDomainName: accountName
    networkAcls: {
      defaultAction: 'Allow'
      virtualNetworkRules: []
      ipRules: []
      bypass: 'AzureServices'
    }
    publicNetworkAccess: 'Enabled'
    networkInjections: null
    disableLocalAuth: false
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' = {
  parent: account
  name: 'fsi-project'
  location: location
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    description: 'FSI Agents Demo'
    displayName: 'FSI'
  }
}

@description('Built-in Role: [Reader]')
resource insight_reader 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: 'acdd72a7-3385-48ef-bd42-f606fba81ae7'
  scope: subscription()
}

module project_insight_reader 'br/public:avm/ptn/authorization/resource-role-assignment:0.1.2' = {
  name: 'project_insight_reader'
  params: {
    principalId: project.identity.principalId
    resourceId: insights.id
    roleDefinitionId: insight_reader.id
  }
}

@description('Built-in Role: [Foundry User]')
resource foundry_user 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '53ca6127-db72-4b80-b1b0-d745d6d5456d'
  scope: subscription()
}

module project_foundry_user 'br/public:avm/ptn/authorization/resource-role-assignment:0.1.2' = {
  name: 'project_foundry_user'
  params: {
    principalId: project.identity.principalId
    resourceId: project.id
    roleDefinitionId: foundry_user.id
  }
}

output resourceName string = account.name
output projectResourceName string = project.name
output projectEndpoint string = 'https://${account.name}.services.ai.azure.com/api/projects/${project.name}'
output projectPrincipalId string = project.identity.principalId
