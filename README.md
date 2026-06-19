# Agent Evaluation & Observability — Azure Foundry End-to-End Demo

https://github.com/user-attachments/assets/bca2055d-c9dc-4c8f-b2f4-75423f2023f4

### Without Evaluation — What Could Go Wrong?

```mermaid
flowchart LR
    A[Developer changes prompt] --> B[Deploy blindly]
    B --> C[Production 💥]

    C -.-> D["⚠️ Hallucinated financial advice sent to clients"]
    C -.-> E["⚠️ Tool calls fail silently — agent invents data"]
    C -.-> F["⚠️ Regression undetected for weeks"]
    C -.-> G["⚠️ No quality baseline — 'it works on my machine'"]
```

### With Azure Foundry Evaluation — Continuous Quality

```mermaid
flowchart LR
    subgraph CICD ["🔄 CI/CD Evaluation"]
        direction LR
        PR[PR Opened] --> RunEval[Run Eval Dataset]
        RunEval --> Compare[Compare Versions]
        Compare --> Gate[Gate Pass/Fail]
    end

    subgraph Sampling ["📊 Sampling — Production Traffic"]
        direction LR
        Live[Live Calls] --> Sample[Sample % Traffic]
        Sample --> Evaluate[Evaluate Quality]
        Evaluate --> Metrics[📈 Metrics]
    end

    subgraph Scheduled ["⏰ Scheduled Evaluation"]
        direction LR
        Cron[Cron / Timer] --> FullTest[Full Test Run]
        FullTest --> Trend[Trend Analysis]
        Trend --> Alerts[🚨 Alerts]
    end
```

> **Result:** Every change measured • Drift detected early • Quality proven

<br/>

---

This repository demonstrates an end-to-end evaluation workflow for AI agents built with Azure Foundry Agent Service. It covers the full lifecycle: creating a versioned agent, connecting tools through MCP, running evaluation datasets, and tracking quality over time.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Documentation Map](#documentation-map)

## Overview

The demo uses a Wealth Advisory Assistant scenario where an agent answers questions about client portfolios, risk profiles, and fund holdings through a remote MCP server.

Evaluation is used as a quality gate so prompt, tool, or infrastructure changes can be measured before promotion to production.

![Evaluation Lifecycle](images/lifecycle.png)

## Quick Start

1. Read the deployment guide in [docs/deployment/README.md](docs/deployment/README.md).
2. Deploy Azure resources with the Create Azure resources workflow.
3. Deploy the MCP server with the Deploy MCP Server workflow.
4. Review the evaluation model and evaluators in [docs/evaluation/README.md](docs/evaluation/README.md).
5. If you run high-concurrency evaluations, apply the MCP runtime reliability guidance in [docs/operations/README.md](docs/operations/README.md).

## Documentation Map

- [docs/overview/README.md](docs/overview/README.md): Project goals, scenario context, and why evaluation matters.
- [docs/evaluation/README.md](docs/evaluation/README.md): Model-based evaluation flow and the 14 evaluators used in this demo.
- [docs/deployment/README.md](docs/deployment/README.md): Step-by-step tenant deployment and GitHub Actions setup.
- [docs/cicd/README.md](docs/cicd/README.md): Agent CI/CD pipeline — versioning, evaluation, and version comparison.
- [docs/operations/README.md](docs/operations/README.md): MCP server reliability guidance, including 503 troubleshooting and gunicorn production tuning.
