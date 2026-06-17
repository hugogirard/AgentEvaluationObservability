# Evaluation

## How Model-Based Evaluation Works

Azure Foundry uses model-based evaluators such as Task Adherence and Coherence to score agent outputs. A judge model reviews each response against criteria and returns quality scores.

![Evaluation Models Diagram](../../images/evaluation-models-diagram.png)

## Evaluators Used in This Demo

This project runs 14 built-in evaluators against the agent, defined in [evaluation/dataset/cicd.json](../../evaluation/dataset/cicd.json). They are grouped into System, Process (tool usage), and General Purpose or RAG quality evaluators.

### System Evaluators

| Evaluator | Purpose | Why It Matters for Agents |
|-----------|---------|---------------------------|
| Task Adherence | Measures whether actions follow rules, procedures, and policy constraints from the system message. | Ensures guardrails are respected in regulated domains. |
| Task Completion | Measures whether the agent completed the full task with a usable deliverable. | Catches responses that acknowledge the request but never fulfill it. |
| Intent Resolution | Measures whether the user's intent is identified and addressed correctly. | Detects intent misunderstandings early. |
| Customer Satisfaction | Measures holistic quality across helpfulness, completeness, clarity, tone, resolution, and adaptability. | Adds a user-centered signal beyond factual correctness. |
| Deflection Rate | Measures how often valid requests are unnecessarily refused. | Detects over-conservative behavior that harms UX. |

### Process Evaluators (Tool Usage)

| Evaluator | Purpose | Why It Matters for Agents |
|-----------|---------|---------------------------|
| Tool Call Accuracy | Measures whether the right tools and parameters are used without redundancy. | Captures tool quality issues in one composite signal. |
| Tool Selection | Measures whether only the necessary tools are selected. | Prevents latency and token waste from irrelevant calls. |
| Tool Input Accuracy | Validates tool parameters for type, format, required fields, and value quality. | Catches subtle parameter bugs. |
| Tool Output Utilization | Measures whether tool results are correctly interpreted and used in the final response. | Catches cases where results are ignored or misread. |
| Tool Call Success | Measures tool execution success and runtime failures. | Detects timeout and exception-driven answer degradation. |

### General Purpose and RAG Evaluators

| Evaluator | Purpose | Why It Matters for Agents |
|-----------|---------|---------------------------|
| Groundedness | Measures whether answers are grounded in retrieved context or tool outputs. | Detects hallucinations. |
| Coherence | Measures logical consistency and flow. | Improves readability and trust. |
| Fluency | Measures language quality and naturalness. | Prevents awkward or low-quality wording. |
| Relevance | Measures response relevance to the prompt. | Detects off-topic responses. |

## References

- [Agent Evaluators documentation](https://learn.microsoft.com/en-us/azure/foundry/concepts/evaluation-evaluators/agent-evaluators)
- [Built-in Evaluators reference](https://learn.microsoft.com/en-us/azure/foundry/concepts/built-in-evaluators)
