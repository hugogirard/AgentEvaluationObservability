from typing import Optional

from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_client_repository
from repository import ClientRepository
from models import Client, Holding

tools = FastMCP(
    "Client Tools",
    instructions="""Tools for managing wealth-advisory client portfolios.
Use these tools to look up client information, query clients by advisor or risk profile,
and manage portfolio holdings (add, remove, update). All monetary values are in CAD.""",
)


@tools.tool()
async def get_client_by_id(
    client_id: str,
    repository: ClientRepository = Depends(get_client_repository),
) -> Client:
    """Retrieve a single client portfolio by their unique client ID.
    Use this to get full details of a specific client including holdings, balances,
    risk profile, and account type.

    Args:
        client_id: The unique client identifier (e.g. "1042", "1105").
    """
    return repository.get_by_id(client_id)


@tools.tool()
async def get_all_clients(
    repository: ClientRepository = Depends(get_client_repository),
) -> list[Client]:
    """List every client portfolio in the system.
    Returns all clients with their full holdings and account details.
    Use this when you need a complete overview of the book of business.
    """
    return repository.get_all()


@tools.tool()
async def get_clients_by_advisor(
    advisor_id: str,
    repository: ClientRepository = Depends(get_client_repository),
) -> list[Client]:
    """Find all clients assigned to a specific advisor.
    Use this to get an advisor's full book of business or to review
    all portfolios under their management.

    Args:
        advisor_id: The advisor identifier (e.g. "ADV-301", "ADV-302").
    """
    return repository.get_by_advisor(advisor_id)


@tools.tool()
async def get_clients_by_risk_profile(
    risk_profile: str,
    repository: ClientRepository = Depends(get_client_repository),
) -> list[Client]:
    """Find all clients matching a given risk profile.
    Use this to identify clients within a specific risk category,
    for example when reviewing portfolio drift across a risk segment.

    Args:
        risk_profile: The risk profile to filter by — "Conservative", "Moderate", or "Aggressive". Case-insensitive.
    """
    return repository.get_by_risk_profile(risk_profile)


@tools.tool()
async def add_client_holding(
    client_id: str,
    fund_code: str,
    fund_name: str,
    units: float,
    market_value: float,
    book_cost: float,
    repository: ClientRepository = Depends(get_client_repository),
) -> Client:
    """Add a new fund holding to a client's portfolio.
    Portfolio weights and total balance are automatically recalculated after the addition.

    Args:
        client_id: The client identifier to add the holding to (e.g. "1042").
        fund_code: The fund code for the new holding (e.g. "GEG-7200", "CDIV").
        fund_name: Display name of the fund (e.g. "Global Equity Growth Fund").
        units: Number of units or shares to add.
        market_value: Current market value in CAD.
        book_cost: Original cost basis in CAD.
    """
    holding = Holding(
        fundCode=fund_code,
        fundName=fund_name,
        units=units,
        marketValue=market_value,
        bookCost=book_cost,
        weight=0.0,
    )
    return repository.add_holding(client_id, holding)


@tools.tool()
async def remove_client_holding(
    client_id: str,
    fund_code: str,
    repository: ClientRepository = Depends(get_client_repository),
) -> Client:
    """Remove a fund holding from a client's portfolio.
    Portfolio weights and total balance are automatically recalculated after the removal.

    Args:
        client_id: The client identifier (e.g. "1042").
        fund_code: The fund code of the holding to remove (e.g. "GEG-7200").
    """
    return repository.remove_holding(client_id, fund_code)


@tools.tool()
async def update_client_holding(
    client_id: str,
    fund_code: str,
    units: Optional[float] = None,
    market_value: Optional[float] = None,
    book_cost: Optional[float] = None,
    repository: ClientRepository = Depends(get_client_repository),
) -> Client:
    """Update an existing holding in a client's portfolio.
    Only provided fields are changed; omitted fields remain as-is.
    Portfolio weights and total balance are automatically recalculated.

    Args:
        client_id: The client identifier (e.g. "1042").
        fund_code: The fund code of the holding to update (e.g. "GEG-7200").
        units: New number of units or shares, or omit to leave unchanged.
        market_value: New market value in CAD, or omit to leave unchanged.
        book_cost: New cost basis in CAD, or omit to leave unchanged.
    """
    return repository.update_holding(client_id, fund_code, units=units, market_value=market_value, book_cost=book_cost)