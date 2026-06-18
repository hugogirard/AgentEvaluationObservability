from typing import Iterator, Optional
from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from dependencies import get_client_repository
from repository import ClientRepository
from models import Client, Holding
from infrastructure.enum import AdvisorId, RiskProfile
from opentelemetry import trace
from opentelemetry.trace import Span
import logging
import os

logger = logging.getLogger(__name__)

if os.getenv('APPLICATIONINSIGHTS_CONNECTION_STRING'):
    tracer = trace.get_tracer('wealth-mcp-server')
else:
    tracer = None    

client_mcp = FastMCP(
    "Client Tools",
    instructions="""Tools for managing wealth-advisory client portfolios.
Use these tools to look up client information, query clients by advisor or risk profile,
and manage portfolio holdings (add, remove, update). All monetary values are in CAD.""",
)


@client_mcp.tool()
async def get_all_clients(
    repository: ClientRepository = Depends(get_client_repository),
) -> list[Client]:
    """List every client portfolio in the system.
    Returns all clients with their full holdings and account details.
    Use this when you need a complete overview of the book of business.
    """

    span_context = tracer.start_as_current_span("mcp_tool_get_all_clients") if tracer else None
    if span_context:
        span_context.__enter__()
        span = trace.get_current_span()      
        span.set_attribute("mcp.tool", "get_all_clients")            

    try:
        return await repository.get_all()
    finally:
        if span_context:
            span_context.__exit__(None,None,None)

@client_mcp.tool()
async def get_client_by_id(
    client_id: str,
    repository: ClientRepository = Depends(get_client_repository),
) -> Client | str:
    """Retrieve a single client portfolio by their unique client ID.
    Use this to get full details of a specific client including holdings, balances,
    risk profile, and account type.

    Args:
        client_id: The unique client identifier (e.g. "1042", "1105").
    """
    span_context = tracer.start_as_current_span("mcp_tool_get_client_by_id") if tracer else None
    if span_context:
        span_context.__enter__()
        span = trace.get_current_span()      
        span.set_attribute("mcp.tool", "get_client_by_id")  
        span.set_attribute("mcp.tool.client_id", client_id)

    try:
        result = await repository.get_by_id(client_id)
        if result is None:
            return f"No client found with ID '{client_id}'."
        return result
    finally:
        if span_context:
            span_context.__exit__(None,None,None)
    


@client_mcp.tool()
async def get_clients_by_advisor(
    advisor_id: str,
    repository: ClientRepository = Depends(get_client_repository),
) -> list[Client] | str:
    """Find all clients assigned to a specific advisor.
    Use this to get an advisor's full book of business or to review
    all portfolios under their management.

    Args:
        advisor_id: The advisor identifier — one of "ADV-118", "ADV-205", or "ADV-301".
    """
    valid_ids = {e.value for e in AdvisorId}
    if advisor_id not in valid_ids:
        return f"Unknown advisor '{advisor_id}'. Valid advisor IDs are: {', '.join(sorted(valid_ids))}."

    span_context = tracer.start_as_current_span("mcp_tool_get_clients_by_advisor") if tracer else None
    if span_context:
        span_context.__enter__()
        span = trace.get_current_span()      
        span.set_attribute("mcp.tool", "get_clients_by_advisor")  
        span.set_attribute("mcp.tool.advisor_id", advisor_id)

    try:
        results = await repository.get_by_advisor(advisor_id)
        if not results:
            return f"No clients found for advisor '{advisor_id}'."
        return results
    finally:
        if span_context:
            span_context.__exit__(None,None,None)
    


@client_mcp.tool()
async def get_clients_by_risk_profile(
    risk_profile: str,
    repository: ClientRepository = Depends(get_client_repository),
) -> list[Client] | str:
    """Find all clients matching a given risk profile.
    Use this to identify clients within a specific risk category,
    for example when reviewing portfolio drift across a risk segment.

    Args:
        risk_profile: The risk profile to filter by — must be one of "Aggressive", "Conservative", or "Moderate". Do NOT pass fund risk levels such as "High", "Low", "Medium", etc. — those are different from client risk profiles.
    """
    valid_profiles = {e.value for e in RiskProfile}
    if risk_profile not in valid_profiles:
        return f"Unknown risk profile '{risk_profile}'. Valid profiles are: {', '.join(sorted(valid_profiles))}."

    span_context = tracer.start_as_current_span("mcp_tool_get_clients_by_risk_profile") if tracer else None
    if span_context:
        span_context.__enter__()
        span = trace.get_current_span()      
        span.set_attribute("mcp.tool", "get_clients_by_risk_profile")  
        span.set_attribute("mcp.tool.risk_profile", risk_profile)
    
    try:
        results = await repository.get_by_risk_profile(risk_profile)
        if not results:
            return f"No clients found with risk profile '{risk_profile}'."
        return results
    finally:
        if span_context:
            span_context.__exit__(None,None,None)
   