# --- API Key Middleware ---
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_headers
from mcp import McpError
from mcp.types import ErrorData
class SubscriptionKeyMiddleware(Middleware):

    def __init__(self, api_key:str):
        self.api_key = api_key

    async def on_message(self, context:MiddlewareContext, call_next):                

        headers = get_http_headers() or {}
        key_value = headers.get('x-mcp-server-key')

        if key_value != self.api_key:
            raise McpError(
                ErrorData(code=-32000, message="Unauthorized: missing or invalid x-mcp-server-key")
            )

        return await call_next(context)        