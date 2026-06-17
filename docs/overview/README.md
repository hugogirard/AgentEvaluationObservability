# Overview

## Goal

Show how to systematically evaluate an AI agent in Azure Foundry, from dataset preparation through evaluation runs, so that every prompt or tool change is validated before reaching production.

## Scenario

The demo uses a Wealth Advisory Assistant scenario: a bank relationship manager asks an agent questions about client portfolios, risk profiles, and fund holdings. The agent calls an MCP server for live data, and evaluation runs measure whether responses are correct and coherent.

## Why Evaluation Matters

Without structured evaluation, AI agent deployments carry significant risks:

| Risk | Impact |
|------|--------|
| Undetected regressions | A prompt tweak that improves one scenario silently breaks others with no immediate signal. |
| Hallucinations go unchecked | The agent can invent data and there is no automated gate to catch it. |
| No baseline for iteration | You cannot tell if version N+1 is better or worse than version N on fixed scenarios. |
| Cannot compare versions objectively | Multiple prompt variants may exist without a reliable winner signal. |
| Compliance and audit risk | Regulated domains require evidence of test coverage and quality gates. |

Evaluation turns agent development from guesswork into an engineering discipline with measurable quality metrics.

## Lifecycle Placement

The diagram below shows where evaluation fits in the Azure Foundry agent lifecycle:

![Evaluation Lifecycle](../../images/lifecycle.png)
