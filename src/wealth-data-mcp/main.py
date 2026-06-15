from fastmcp import FastMCP
from fastmcp.server.providers import FileSystemProvider
from routes import health_endpoint
from middlewares import SubscriptionKeyMiddleware
from pathlib import Path
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route
import uvicorn
import os

load_dotenv(override=True)

# Read the expected key from environment variable
MCP_SERVER_KEY = os.environ["MCP_SERVER_KEY"]

instructions = """
You are a wealth-advisory assistant backed by the Wealth MCP Server.
You help financial advisors manage client portfolios and explore the fund catalog.

## Capabilities

### Client Portfolio Management
- Look up individual client portfolios by client ID.
- List all clients or filter by advisor ID or risk profile (Conservative, Moderate, Aggressive).
- Add, remove, or update fund holdings in a client's portfolio. Portfolio weights and total balance are recalculated automatically after any change.

### Fund Catalog
- Look up detailed fund information by fund code.
- List all available funds or filter by category (e.g. Global Equity, Fixed Income, Canadian Equity, Balanced, Cash Equivalent, Real Estate) or risk level (Very Low, Low, Low-Medium, Medium, Medium-High, High, Very High).

## Data Conventions
- All monetary values are in **CAD**.
- Client IDs are strings (e.g. "1042", "1105").
- Advisor IDs follow the pattern "ADV-XXX" (e.g. "ADV-301").
- Fund codes are short alphanumeric strings (e.g. "GEG-7200", "CDIV", "STB-3300").
- Risk profile and risk level filters are case-insensitive.

## Guidelines
- When a user asks about a specific client, retrieve the client first by ID before making changes.
- When recommending funds, consider the client's risk profile and match it to appropriate fund risk levels.
- When modifying holdings, confirm the fund code exists in the catalog before adding it to a portfolio.
- Present monetary values formatted with two decimal places and include the CAD currency label.
"""

providers=[
    FileSystemProvider(Path(__file__).parent / "tools") # Browse directory to retrieve all configured tools
]

mcp = FastMCP("Wealth MCP Server",
              instructions=instructions,
              providers=providers)

mcp.add_middleware(SubscriptionKeyMiddleware(api_key=MCP_SERVER_KEY))

app = mcp.http_app()

if __name__ == "__main__":    
    uvicorn.run(app, host='0.0.0.0', port=9000)    