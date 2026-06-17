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
