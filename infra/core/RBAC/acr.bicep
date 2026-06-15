param acrResourceId string
param principalId string

@description('Built-in Role: [AcrPull]')
resource acr_pull 'Microsoft.Authorization/roleDefinitions@2022-04-01' existing = {
  name: '7f951dda-4ed3-4680-a7ca-43fe172d538d'
  scope: subscription()
}

module webArcPull 'br/public:avm/ptn/authorization/resource-role-assignment:0.1.2' = {
  name: 'webArcPull'
  params: {
    principalId: principalId
    resourceId: acrResourceId
    roleDefinitionId: acr_pull.id
  }
}
