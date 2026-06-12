using 'main.bicep'

param environmentName = 'contoso-bank'

param location = 'canadaeast'

param resourceGroupName = 'rg-fsi-demo-eval'

param chatCompleteionDeploymentName = 'gpt-5-mini'

param chatDeploymentSku = 'GlobalStandard'

param chatModelProperties = {
  format: 'OpenAI'
  name: 'gpt-5.4'
  version: '2026-03-05'
}

param chatModelSkuCapacity = 150

param embeddingDeploymentName = 'text-embedding-3-large'

param embeddingDeploymentSku = 'GlobalStandard'

param embeddingModelProperties = {
  format: 'OpenAI'
  name: 'text-embedding-3-large'
  version: '1'
}

param embeddingModelSkuCapacity = 150
