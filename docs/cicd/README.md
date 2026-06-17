# Agent CI/CD

The **Configure Wealth Agent** workflow ([`.github/workflows/agent.yaml`](../../.github/workflows/agent.yaml)) automates agent versioning and evaluation in a single pipeline. It is triggered manually via `workflow_dispatch` and contains two sequential jobs.

## Job 1 — Configure Foundry Agent

**Job name:** `configure-foundry-agents`

This job creates a new versioned agent in Azure Foundry and persists version metadata for the evaluation job.

### Steps

1. **Checkout & setup** — checks out the repository, installs Python 3.11, and sets up `uv` for dependency management.
2. **Install dependencies** — runs `uv sync` inside the `agents/` directory to install the agent creation script dependencies.
3. **Azure Login** — authenticates to the Azure tenant using the `AZURE_CREDENTIALS` service principal secret.
4. **Run agent creation script** — executes `agents/main.py`, which:
   - Connects to the Foundry project using `PROJECT_ENDPOINT`.
   - Looks up the existing MCP server connection (`WEALTH-MCP-SERVER`).
   - Retrieves the most recent agent version (if any) for later comparison.
   - Creates a new agent version with the current prompt (`agents/prompt.txt`) and MCP tool configuration.
   - Outputs a comma-separated list of agent versions (previous + new) as `AGENT_VERSIONS`, e.g. `WealthAgent:3,WealthAgent:4`.
5. **Save agent version as secret** — persists `AGENT_VERSIONS` to a repository secret using the `PA_TOKEN` so downstream workflows and future runs can reference it.

### What triggers a new version?

Any change to the agent prompt, tool wiring, or model configuration results in a new Foundry agent version when the workflow runs. Because Foundry agents are immutable and versioned, the previous version remains available for comparison.

In a production setup, this workflow should be triggered automatically on any code change (e.g. on `push` or `pull_request` to `main`) rather than manually via `workflow_dispatch`. This ensures every change is versioned and evaluated before promotion.

## Job 2 — Run Agent Evaluations

**Job name:** `run-agent-evaluations`

This job depends on Job 1 (`needs: configure-foundry-agents`) and runs the evaluation suite using the [`microsoft/ai-agent-evals`](https://github.com/microsoft/ai-agent-evals) GitHub Action.

### Inputs

| Input | Source | Description |
|-------|--------|-------------|
| `azure-ai-project-endpoint` | `PROJECT_ENDPOINT` secret | Foundry project endpoint |
| `deployment-name` | `CHAT_COMPLETION_MODEL` secret | Model deployment used as the judge |
| `agent-ids` | Job 1 output | Comma-separated agent versions to evaluate (e.g. `WealthAgent:3,WealthAgent:4`) |
| `data-path` | `evaluation/dataset/cicd.json` | Evaluation dataset with queries and evaluator configuration |

### How version comparison works

The agent creation script (`agents/main.py`) retrieves the latest existing version before creating the new one. Both versions are passed to the evaluation action as `agent-ids`. The evaluation action runs every query from the dataset against **each version independently**, then produces side-by-side results so you can compare quality metrics between the previous and new versions.

This means every pipeline run answers the question: *"Did this change make the agent better or worse?"*

### Evaluators

The evaluation dataset (`evaluation/dataset/cicd.json`) configures 14 built-in evaluators, each with a passing threshold of 3:

| Evaluator | What it measures |
|-----------|-----------------|
| `groundedness` | Are responses grounded in retrieved data? |
| `fluency` | Is the language natural and well-formed? |
| `coherence` | Is the response logically consistent? |
| `tool_selection` | Did the agent pick the right tool? |
| `tool_output_utilization` | Did the agent use the tool output effectively? |
| `tool_input_accuracy` | Were the tool inputs correct? |
| `tool_call_success` | Did the tool call succeed? |
| `task_completion` | Did the agent complete the requested task? |
| `task_adherence` | Did the agent follow its instructions? |
| `relevance` | Is the response relevant to the query? |
| `intent_resolution` | Did the agent correctly understand user intent? |
| `tool_call_accuracy` | Were tool calls accurate overall? |
| `tool_call_success` | Did the tool calls execute successfully? |
| `task_completion` | Did the agent fully complete the task? |

### Test queries

The dataset includes a mix of:

- **Off-topic queries** (e.g. "Tell me about Tokyo Disneyland") to test guardrails and task adherence.
- **Client lookups** by ID and name to verify tool selection and data retrieval.
- **Advisor-scoped queries** to test filtering logic.
- **Fund catalog queries** to validate catalog search and risk-based filtering.
- **Portfolio modification queries** to verify end-to-end write operations.

## Execution time

A full pipeline run typically takes **15–20 minutes**. The majority of the time is spent in Job 2, where each query is sent to every agent version and scored by all 14 evaluators using the judge model.

## Viewing results

After the workflow completes, evaluation results are available in:

1. **GitHub Actions logs** — the evaluation action prints summary metrics in the workflow output.
2. **Azure Foundry portal** — navigate to your Foundry project to view detailed evaluation runs, per-query scores, and version comparison dashboards.
