targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('The name of the resource group')
param resourceGroupName string

@description('The model for the chat completion')
param chatCompleteionDeploymentName string

@description('The SKU of the chat completion model')
param chatDeploymentSku string

@description('The properties of the chat model')
param chatModelProperties object

@description('The chat model SKU capacity')
param chatModelSkuCapacity int

@description('The embedding deployment name')
param embeddingDeploymentName string

@description('The embedding deployment SKU')
param embeddingDeploymentSku string

@description('The embedding model properties')
param embeddingModelProperties object

@description('The embedding model SKU capacity')
param embeddingModelSkuCapacity int

// tags that should be applied to all resources.
var tags = {
  // Tag all resources with the environment name.
  'azd-env-name': environmentName
  SecurityControl: 'Ignore'
}

var abbrs = loadJsonContent('./abbreviations.json')

var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

module aisearch 'core/ai/search.bicep' = {
  scope: rg
  params: {
    location: location
    tags: tags
    aiSearchResourceName: '${abbrs.searchSearchServices}${resourceToken}'
  }
}

module foundry 'core/ai/foundry.bicep' = {
  scope: rg
  params: {
    location: location
    accountName: '${abbrs.cognitiveServicesAccounts}${resourceToken}'
    tags: tags
  }
}

module chatCompletionModel 'core/ai/model.deployment.bicep' = {
  scope: rg
  params: {
    aiFoundryAccountName: foundry.outputs.resourceName
    deploymentName: chatCompleteionDeploymentName
    deploymentSku: chatDeploymentSku
    modelProperties: chatModelProperties
    skuCapacity: chatModelSkuCapacity
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
  }
}

module embeddingnModel 'core/ai/model.deployment.bicep' = {
  scope: rg
  params: {
    aiFoundryAccountName: foundry.outputs.resourceName
    deploymentName: embeddingDeploymentName
    deploymentSku: embeddingDeploymentSku
    modelProperties: embeddingModelProperties
    skuCapacity: embeddingModelSkuCapacity
    versionUpgradeOption: 'NoAutoUpgrade'
  }
  dependsOn: [
    chatCompletionModel // To avoid deployment concurrency and fail the bicep
  ]
}

module storage 'core/data/storage.bicep' = {
  scope: rg
  params: {
    location: location
    tags: tags
    storageResourceName: '${abbrs.storageStorageAccounts}${resourceToken}'
  }
}

module registry 'core/container/registry.bicep' = {
  scope: rg
  params: {
    location: location
    tags: tags
    resourceName: '${abbrs.containerRegistryRegistries}${resourceToken}'
  }
}

module webfarm 'core/web/webfarm.bicep' = {
  scope: rg
  params: {
    location: location
    resourceName: '${abbrs.webServerFarms}${resourceToken}'
  }
}

module mcpServer 'core/web/web.bicep' = {
  scope: rg
  params: {
    location: location
    resourceName: '${abbrs.webSitesAppService}mcp-${resourceToken}'
    serverFarmId: webfarm.outputs.resourceId
  }
}

module rbac 'core/RBAC/acr.bicep' = {
  scope: rg
  params: {
    acrResourceId: registry.outputs.resourceId
    principalId: mcpServer.outputs.principalId
  }
}

output CONTAINER_REGISTRY_NAME string = registry.outputs.resourceName
output MCP_SERVER_NAME string = mcpServer.outputs.resourceName
