# Deployment

## 1. Fork the Repository

Fork this repository into your own GitHub account or organization.

## 2. Create a Service Principal and Save as Secret

The GitHub Actions workflow uses Azure/login@v2 to authenticate to your tenant.

1. Create a service principal with contributor access:

```bash
az ad sp create-for-rbac --name "github-agent-eval" \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID> \
  --sdk-auth
```

2. Copy the full JSON output.
3. In your fork, go to Settings -> Secrets and variables -> Actions.
4. Create a secret named AZURE_CREDENTIALS with that JSON value.

## 3. Create a Personal Access Token

The workflow needs write access to repository secrets to persist agent version metadata.

1. Go to GitHub Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens.
2. Scope to your forked repository.
3. Set Repository permissions -> Secrets to Read and write.
4. Create a repository secret named PA_TOKEN using that token value.

## 4. Run Create Azure resources Workflow

Go to Actions -> Create Azure resources -> Run workflow on main.

This provisions infrastructure from [infra/main.bicep](../../infra/main.bicep):

| Resource | Purpose |
|----------|---------|
| Azure Foundry project | Hosts the AI agent and evaluation runs |
| AI model deployment | Chat model for runtime and judge model for evaluation |
| Azure Container Registry | Stores MCP server images |
| Azure App Service | Hosts MCP server container |
| Azure Cosmos DB | Stores client and fund data |
| Azure Monitor | Observability and tracing |

The workflow also writes these repository secrets:

- CONTAINER_REGISTRY_NAME
- MCP_SERVER_NAME
- PROJECT_ENDPOINT
- CHAT_COMPLETION_MODEL

## 5. Run Load Data in CosmosDB Workflow

Go to Actions -> Load data in CosmosDB -> Run workflow on main.

This workflow seeds the Cosmos DB database with client and fund data required by the MCP server. It retrieves the connection string at runtime using the `COSMOS_DB_RESOURCE_NAME` and `RESOURCE_GROUP_NAME` secrets (set automatically by Step 4), then runs `utility/load_data.py` to populate the collections.

## 6. Run Deploy MCP Server Workflow

Go to Actions -> Deploy MCP Server -> Run workflow on main.

This workflow:

1. Builds the Docker image from src/wealth-data-mcp.
2. Pushes tags (commit SHA and latest) to ACR.
3. Deploys the image to the App Service.

After deployment, the MCP server exposes portfolio tools used by the Foundry agent during runtime and evaluation.

## 7. Run Configure Wealth Agent Workflow

Go to Actions -> Configure Wealth Agent -> Run workflow on main.

This workflow contains two jobs that create a new agent version and automatically evaluate it against the previous one. The full CI/CD process is described in the [Agent CI/CD Guide](../cicd/README.md).

> **Note:** This workflow can take up to 20 minutes to complete, mainly due to the evaluation job which runs 14 evaluators across every query in the dataset for each agent version.
