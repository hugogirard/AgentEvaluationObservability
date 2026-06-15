# CosmosDB Dataset for MCP Server

This folder contains JSON data files to import into Azure Cosmos DB (NoSQL API). These back the three MCP server tools used by the Wealth Advisory Assistant agent.

## Database

| Property       | Value              |
|----------------|--------------------|
| **Database**   | `wealth-advisory`  |
| **API**        | NoSQL              |
| **Throughput** | 400 RU/s (shared)  |

---

## Containers

### 1. `clients`

| Property          | Value        |
|-------------------|--------------|
| **Partition Key** | `/clientId`  |
| **Data File**     | `clients.json` |
| **Documents**     | 10           |

Stores client portfolio data: holdings, asset allocation, balances, and risk profile.

**MCP Tool:** `get_client_portfolio(client_id)`

**Query:**

```sql
SELECT * FROM c WHERE c.clientId = @clientId
```

**Example:** `get_client_portfolio("1042")` returns Margaret Chen's portfolio — 80% equities / 20% fixed income with a Moderate risk profile (deliberately drifted for demo).

**Document schema:**

| Field                  | Type     | Description                                       |
|------------------------|----------|---------------------------------------------------|
| `id`                   | string   | Cosmos DB document id (`client-{clientId}`)       |
| `clientId`             | string   | Client identifier (partition key)                 |
| `name`                 | string   | Client full name                                  |
| `riskProfile`          | string   | `Conservative` \| `Moderate` \| `Aggressive`      |
| `accountType`          | string   | `RRSP` \| `TFSA` \| `Non-Registered` \| `RRIF`   |
| `advisorId`            | string   | Assigned advisor identifier                       |
| `lastReviewDate`       | string   | ISO date of last portfolio review                 |
| `totalBalance`         | number   | Total portfolio market value (CAD)                |
| `holdings[]`           | array    | Array of position objects                         |
| `holdings[].fundCode`  | string   | Fund code (BGF-4501, GIC-1800, CDIV, GEG-7200, STB-3300) |
| `holdings[].fundName`  | string   | Fund display name                                 |
| `holdings[].units`     | number   | Units/shares held                                 |
| `holdings[].marketValue` | number | Current market value (CAD)                       |
| `holdings[].bookCost`  | number   | Original cost basis (CAD)                         |
| `holdings[].weight`    | number   | Percentage of total portfolio                     |
| `assetAllocation`      | object   | Breakdown by asset class (percentages)            |
| `totalEquityPercent`   | number   | Total equity allocation                           |
| `totalFixedIncomePercent` | number | Total fixed income allocation                   |

**Clients with deliberate drift** (for rebalancing demo scenarios):

| Client ID | Name           | Profile      | Issue                                   |
|-----------|----------------|--------------|----------------------------------------|
| 1042      | Margaret Chen  | Moderate     | 80/20 equity-heavy (target ~50/50)     |
| 1340      | Lisa Patel     | Aggressive   | 83.9% in single fund — concentration risk |
| 1508      | Emma Dubois    | Moderate     | 82.1% equities, heavy international tilt |
| 1701      | Anne Bergström | Conservative | 100% GIC — maturing, needs reinvestment |
| 1845      | Raj Kapoor     | Moderate     | 72.8% fixed income — underinvested     |

---

### 2. `marketSummaries`

| Property          | Value             |
|-------------------|-------------------|
| **Partition Key** | `/assetClass`     |
| **Data File**     | `market_summaries.json` |
| **Documents**     | 6                 |

Stores current-day market snapshot per asset class.

**MCP Tool:** `get_market_summary(asset_class)`

**Query:**

```sql
SELECT * FROM c WHERE c.assetClass = @assetClass
```

**Example:** `get_market_summary("equities")` — the MCP server maps `"equities"` to the relevant asset class keys (`canadian_equities`, `us_equities`, `international_equities`) or returns all of them.

**Valid `assetClass` values:**

| Asset Class               | Index Tracked                 | Trend   |
|---------------------------|-------------------------------|---------|
| `canadian_equities`       | S&P/TSX Composite             | bearish |
| `us_equities`             | S&P 500                       | bearish |
| `international_equities`  | MSCI EAFE                     | neutral |
| `canadian_bonds`          | FTSE Canada Universe Bond     | bullish |
| `corporate_bonds`         | FTSE Canada Corporate Bond    | neutral |
| `cash_equivalents`        | FTSE Canada 91 Day T-Bill     | neutral |

**Document schema:**

| Field                | Type   | Description                              |
|----------------------|--------|------------------------------------------|
| `id`                 | string | Cosmos DB document id                    |
| `assetClass`         | string | Asset class key (partition key)          |
| `date`               | string | Snapshot date (ISO)                      |
| `indexName`          | string | Benchmark index name                     |
| `indexLevel`         | number | Index closing level                      |
| `dailyChangePercent` | number | Day-over-day change (%)                  |
| `ytdReturnPercent`   | number | Year-to-date return (%)                  |
| `volatility30Day`    | number | 30-day rolling volatility                |
| `trend`              | string | `bullish` \| `bearish` \| `neutral`      |
| `commentary`         | string | Analyst-style market summary             |

> **Note:** Equity markets show elevated volatility (22-24) to support the scenario where the agent detects unfavorable conditions and recommends rebalancing.

---

### 3. `riskFactors`

| Property          | Value           |
|-------------------|-----------------|
| **Partition Key** | `/id`           |
| **Data File**     | `risk_factors.json` |
| **Documents**     | 1               |

Single reference document containing risk scoring weights, compliance thresholds, target allocations, and drift rules. Used as a lookup table by the `calculate_risk_score` tool.

**MCP Tool:** `calculate_risk_score(portfolio)`

**Query:**

```sql
SELECT * FROM c WHERE c.id = "risk_factors"
```

The MCP server reads this document, then computes the risk score in application code:

```
risk_score = Σ (asset_class_weight_% × asset_class_risk_factor) / 100
```

**Example:** A portfolio with 80% Canadian Equities (factor 50) and 20% Canadian Bonds (factor 20):

```
risk_score = (0.80 × 50) + (0.20 × 20) = 40 + 4 = 44  →  "Moderate" (21-45)
```

**Document contents:**

| Section                | Description                                                |
|------------------------|------------------------------------------------------------|
| `assetClassRiskWeights`| Risk factor (1-100) per asset class                        |
| `complianceThresholds` | Score ranges → risk profile mapping + max equity %         |
| `targetAllocations`    | Ideal allocation per profile (Conservative/Moderate/Aggressive) |
| `driftThresholds`      | Minor (5-9%) → Critical (20%+) with required actions       |
| `concentrationLimits`  | Max 10% single security, max 25% single sector             |

---

## Importing Data

### Azure Portal

1. Navigate to your Cosmos DB account → **Data Explorer**
2. Create database `wealth-advisory` with shared throughput (400 RU/s)
3. Create each container with the partition keys listed above
4. For each container, click **Items** → **Upload Item** → select the corresponding JSON file

### Azure CLI

```bash
# Create the database
az cosmosdb sql database create \
  --account-name <account> \
  --resource-group <rg> \
  --name wealth-advisory \
  --throughput 400

# Create containers
az cosmosdb sql container create \
  --account-name <account> \
  --resource-group <rg> \
  --database-name wealth-advisory \
  --name clients \
  --partition-key-path "/clientId"

az cosmosdb sql container create \
  --account-name <account> \
  --resource-group <rg> \
  --database-name wealth-advisory \
  --name marketSummaries \
  --partition-key-path "/assetClass"

az cosmosdb sql container create \
  --account-name <account> \
  --resource-group <rg> \
  --database-name wealth-advisory \
  --name riskFactors \
  --partition-key-path "/id"
```

> **Note:** `clients.json` and `market_summaries.json` are JSON arrays — the Cosmos DB Portal upload handles arrays by importing each element as a separate document. If using the SDK or CLI bulk import, iterate over the array items.

---

## Fund Code Reference

All holdings in `clients.json` use fund codes from the bank's product sheets:

| Fund Code  | Product Name                  | Type        | MER   |
|------------|-------------------------------|-------------|-------|
| BGF-4501   | Balanced Growth Fund          | Mutual Fund | 1.85% |
| GIC-1800   | Premium GIC 18-Month          | GIC         | N/A   |
| CDIV       | Canadian Dividend ETF         | ETF         | 0.22% |
| GEG-7200   | Global Equity Growth Fund     | Mutual Fund | 2.15% |
| STB-3300   | Short-Term Bond Fund          | Mutual Fund | 0.95% |
