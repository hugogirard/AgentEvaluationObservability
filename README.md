# Agent Evaluation & Observability — Azure Foundry End-to-End Demo

This repository demonstrates an **end-to-end evaluation workflow for AI agents** built with [Azure Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/). It covers the full cycle: creating a versioned agent, connecting it to tools via MCP, uploading evaluation datasets, defining quality evaluators, and running evaluation passes to measure agent performance over time.

## Goal

Show how to systematically evaluate an AI agent in Azure Foundry — from dataset preparation through evaluation runs — so that every prompt or tool change is validated before reaching production.

The demo uses a **Wealth Advisory Assistant** scenario: a bank relationship manager asks an agent questions about client portfolios, risk profiles, and fund holdings. The agent calls an MCP server for live data, and evaluation runs measure whether the responses are correct and coherent.

## Why Evaluation Matters — The Risks of Skipping It

Without a structured evaluation practice, AI agent deployments carry significant risks:

| Risk | Impact |
|------|--------|
| **Undetected regressions** | A prompt tweak that improves one scenario silently breaks five others — with no signal until users complain. |
| **Hallucinations go unchecked** | The agent invents data (e.g., fictitious portfolio values) and there is no automated gate to catch it. |
| **No baseline for iteration** | Without scores on a fixed dataset, you cannot tell whether version N+1 is better or worse than version N. |
| **Cannot compare agent versions** | Multiple prompt variants exist but there is no objective way to pick the winner. |
| **Compliance & audit risk** | In regulated domains (wealth advisory, healthcare, legal) you need evidence that the system was tested — not just "it looked fine in the playground." |

Evaluation turns agent development from guesswork into an engineering discipline with measurable quality gates.

## Evaluation in the Agent Lifecycle

The diagram below shows where evaluation fits within the Azure Foundry agent development lifecycle:

![Evaluation Lifecycle](images/lifecycle.png)

## How Model-Based Evaluation Works

Azure Foundry uses model-based evaluators (such as **Task Adherence** and **Coherence**) to score agent outputs. A judge model reviews each response against defined criteria and returns a quality score:

![Evaluation Models Diagram](images/evaluation-models-diagram.png)

## Evaluators Used in This Demo

This project runs **14 built-in evaluators** against the agent (defined in [`evaluation/dataset/cicd.json`](evaluation/dataset/cicd.json)). They split into three categories: **System evaluation** (end-to-end outcomes), **Process evaluation** (step-by-step tool usage), and **General purpose / RAG quality** (response linguistics and grounding).

### System Evaluators

| Evaluator | Purpose | Why It Matters for Agents |
|-----------|---------|---------------------------|
| **Task Adherence** | Measures if the agent's actions adhere to its assigned tasks according to rules, procedures, and policy constraints defined in its system message. | Ensures the agent respects guardrails — critical in regulated domains like wealth advisory where deviation from compliance rules is unacceptable. |
| **Task Completion** | Measures if the agent completed the requested task end-to-end with a usable deliverable that meets all user requirements. | Catches cases where the agent acknowledges a request but never actually fulfills it (e.g., says "I'll look that up" but returns no data). |
| **Intent Resolution** | Measures whether the agent correctly identifies and addresses the user's intent. | Detects misunderstandings — e.g., the user asks about a client's risk profile but the agent returns fund information instead. |
| **Customer Satisfaction** | Measures holistic user satisfaction across six dimensions: helpfulness, completeness, clarity, tone, resolution, and adaptability. | Provides a user-centric quality signal beyond technical correctness — the response can be factually right but poorly presented. |
| **Deflection Rate** | Measures how often the agent deflects or refuses to answer a question it should handle. | Identifies over-conservative behavior where the agent unnecessarily declines valid queries, hurting user experience. |

### Process Evaluators (Tool Usage)

| Evaluator | Purpose | Why It Matters for Agents |
|-----------|---------|---------------------------|
| **Tool Call Accuracy** | Measures whether the agent made the right tool calls with correct parameters without redundancy. | The composite score — catches all tool-related issues in one metric: wrong tool, wrong parameters, or unnecessary calls. |
| **Tool Selection** | Measures whether the agent selected the correct and necessary tools without selecting unnecessary ones. | Detects when the agent calls irrelevant tools (e.g., calling `get_all_clients` when it only needs one client by ID), wasting latency and tokens. |
| **Tool Input Accuracy** | Validates that all tool call parameters are correct across strict criteria: groundedness, type compliance, format, required params, no unexpected params, and value appropriateness. | Catches subtle bugs — e.g., passing a client name where a client ID is expected, or sending an integer as a string. |
| **Tool Output Utilization** | Measures if the agent correctly understood and used tool call results contextually in its reasoning and final response. | Detects when the agent calls the right tool but then ignores or misinterprets the returned data in its answer. |
| **Tool Call Success** | Measures if tool calls succeeded or resulted in technical errors or exceptions. | Catches runtime failures (timeouts, 404s, malformed requests) that silently degrade agent answers. |

### General Purpose & RAG Evaluators

| Evaluator | Purpose | Why It Matters for Agents |
|-----------|---------|---------------------------|
| **Groundedness** | Measures how grounded the response is in the retrieved context (tool outputs / knowledge base). | Detects hallucinations — the agent fabricates portfolio values or fund names not present in the actual data. |
| **Coherence** | Measures logical consistency and flow of responses. | Ensures the agent produces structured, readable answers rather than disjointed fragments of data. |
| **Fluency** | Measures natural language quality and readability. | Catches garbled or unnatural phrasing that undermines user trust even when the content is correct. |
| **Relevance** | Measures how relevant the response is with respect to the query. | Identifies off-topic answers — e.g., the user asks about a specific client and the agent responds with generic financial advice. |

> **Reference:** [Agent Evaluators documentation](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators) · [Built-in Evaluators reference](https://learn.microsoft.com/en-us/azure/foundry/concepts/built-in-evaluators)

## Deploy to Your Tenant

### 1. Fork the Repository

Fork this repository into your own GitHub account or organization by clicking **Fork** at the top-right of the repo page.

### 2. Create a Service Principal and Save as Secret

The GitHub Actions workflow uses [`Azure/login@v2`](https://github.com/Azure/login/#login-with-a-service-principal-secret) to authenticate against your Azure tenant.

1. Create a Service Principal with contributor access to your subscription:

   ```bash
   az ad sp create-for-rbac --name "github-agent-eval" \
     --role contributor \
     --scopes /subscriptions/<SUBSCRIPTION_ID> \
     --sdk-auth
   ```

2. Copy the full JSON output. It looks like this:

   ```json
   {
     "clientId": "<GUID>",
     "clientSecret": "<SECRET>",
     "subscriptionId": "<GUID>",
     "tenantId": "<GUID>",
     ...
   }
   ```

3. In your forked repository, go to **Settings → Secrets and variables → Actions → New repository secret**.
4. Create a secret named **`AZURE_CREDENTIALS`** and paste the JSON output as the value.

### 3. Create a Personal Access Token (PAT)

The workflow needs write access to repository secrets to persist the agent version after creation.

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
2. Configure the token:
   - **Repository access:** Select your forked repository only.
   - **Permissions → Repository permissions → Secrets** → Set to **Read and write**.
3. Click **Generate token** and copy the value.
4. In your forked repository, go to **Settings → Secrets and variables → Actions → New repository secret**.
5. Create a secret named **`PA_TOKEN`** and paste the token value.

### 4. Run the "Create Azure resources" Workflow

Once your secrets are configured, trigger the infrastructure deployment:

1. Go to **Actions → Create Azure resources → Run workflow** (select the `main` branch).

This workflow provisions all required Azure resources in your subscription using Bicep templates (`infra/main.bicep`). It creates:

| Resource | Purpose |
|----------|---------|
| **Azure Foundry project** | Hosts the AI agent and evaluation runs |
| **AI model deployment** | Chat completion model used by the agent and as the evaluation judge |
| **Azure Container Registry** | Stores the Docker image for the MCP server |
| **Azure App Service** | Runs the MCP server container (wealth data API) |
| **Azure Cosmos DB** | Data store for client and fund information |
| **Azure Monitor** | Observability and tracing for agent interactions |

After deployment completes, the workflow automatically saves the following values as repository secrets (using your `PA_TOKEN`):

- **`CONTAINER_REGISTRY_NAME`** — ACR name for pushing the MCP server image
- **`MCP_SERVER_NAME`** — App Service name for the MCP server
- **`PROJECT_ENDPOINT`** — Azure Foundry project endpoint (used by the agent and evaluation workflows)
- **`CHAT_COMPLETION_MODEL`** — Deployed model name (used for agent creation and evaluation)

> **Note:** This workflow also runs automatically on any push to `main` that modifies files under `infra/`.

### 5. Run the "Deploy MCP Server" Workflow

Once the infrastructure is provisioned, deploy the MCP server that provides the agent with wealth data tools:

1. Go to **Actions → Deploy MCP Server → Run workflow** (select the `main` branch).

This workflow:

1. **Builds** the Docker image from `src/wealth-data-mcp/` using Azure Container Registry (ACR build).
2. **Pushes** the image to your ACR tagged with the commit SHA and `latest`.
3. **Deploys** the container to the Azure App Service created in the previous step.

After this completes, the MCP server is live and exposes tools like `get_all_clients`, `get_client_by_id`, and `get_clients_by_risk_profile` — which the Foundry agent will call via a remote MCP connection during evaluation.

> **Note:** This workflow also runs automatically on any push to `main` that modifies files under `src/wealth-data-mcp/`.
