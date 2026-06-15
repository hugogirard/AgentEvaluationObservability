from starlette.responses import JSONResponse

# ============================================================================
# HEALTH CHECK ENDPOINT (Unauthenticated)
# ============================================================================

async def health_endpoint(request):
    """Health check endpoint - does not require authentication."""
    return JSONResponse({
        "status": "healthy",
        "server": "Wealth MCP Server"
    })