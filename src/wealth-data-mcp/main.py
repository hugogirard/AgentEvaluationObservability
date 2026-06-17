from fastmcp import FastMCP
from fastmcp.server.providers import FileSystemProvider
from routes import health_endpoint
from middlewares import SubscriptionKeyMiddleware
from pathlib import Path
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from azure.monitor.opentelemetry import configure_azure_monitor
from starlette.routing import Route
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn
import os
import logging

load_dotenv(override=True)

if os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING'):
    configure_azure_monitor(
        connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"],
        logger_name="wealth-mcp-server",
    )

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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

# This is a known issue in the MCP Python SDK. Key issues on modelcontextprotocol/python-sdk:

# 2349 — "Streamable HTTP transport rejects Accept: text/event-stream without application/json" (still open)
# https://github.com/modelcontextprotocol/python-sdk/issues/2349
# Seems foundry client sent this sometimes

class FixAcceptHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/mcp":
            # Ensure both required content types are in Accept
            accept = request.headers.get("accept", "")
            if "text/event-stream" not in accept or "application/json" not in accept:
                # Mutate the scope to include the required Accept header
                raw_headers = [(k, v) for k, v in request.scope["headers"] if k != b"accept"]
                raw_headers.append((b"accept", b"application/json, text/event-stream"))
                request.scope["headers"] = raw_headers
        return await call_next(request)

app = mcp.http_app()
app.add_middleware(FixAcceptHeaderMiddleware)

if __name__ == "__main__":    
    uvicorn.run(app, host='0.0.0.0', port=9000)    