# Scenario: Wealth Advisory Assistant

A relationship manager at a bank asks the agent questions about client portfolios and the bank's investment products. The agent uses two tools to answer:

**Foundry IQ (Knowledge Base)** — vectorized documents containing:

- Product fact sheets (e.g., mutual funds, GICs, ETFs offered by the bank)
- Internal investment policies and suitability guidelines
- FAQ documents on fees, minimum investments, and redemption rules

**MCP Server** — exposes 2-3 simple tools:

- `get_client_portfolio(client_id)` — returns a client's current holdings (asset allocation, balances)
- `get_market_summary(asset_class)` — returns current-day summary for an asset class (equities, fixed income, etc.)
- `calculate_risk_score(portfolio)` — computes a simple risk score from a portfolio's allocation

## Example conversation flow:

> **User:** "Client 1042 is asking about rebalancing. What do you recommend?"
>
> **Agent:**
>
> 1. Calls `get_client_portfolio("1042")` → learns the client is 80% equities / 20% fixed income
> 2. Calls `get_market_summary("equities")` → sees elevated volatility
> 3. Searches Foundry IQ for the bank's suitability guidelines → finds that a "moderate" risk profile should target 60/40
> 4. Calls `calculate_risk_score(...)` → confirms the current portfolio exceeds the client's risk tolerance
> 5. Responds with a recommendation citing the bank's policy and current market conditions