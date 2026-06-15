from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from dependencies import get_fund_repository
from repository import FundRepository
from models import Fund

tools = FastMCP(
    "Fund Tools",
    instructions="""Tools for querying the wealth-advisory fund catalog.
Use these tools to look up fund details, browse funds by category or risk level,
and retrieve NAV, MER, YTD returns, and minimum investment requirements. All monetary values are in CAD.""",
)


@tools.tool()
async def get_fund_by_code(
    fund_code: str,
    repository: FundRepository = Depends(get_fund_repository),
) -> Fund:
    """Retrieve detailed information for a single fund by its code.
    Use this to get full fund details including name, category, risk level, MER,
    NAV per unit, YTD return, minimum investment, and description.

    Args:
        fund_code: The unique fund code (e.g. "GEG-7200", "CDIV", "STB-3300").
    """
    return repository.get_by_code(fund_code)


@tools.tool()
async def get_all_funds(
    repository: FundRepository = Depends(get_fund_repository),
) -> list[Fund]:
    """List all available funds in the catalog.
    Returns every fund with full details including MER, NAV, and performance data.
    Use this when you need a complete view of the product shelf.
    """
    return repository.get_all()


@tools.tool()
async def get_funds_by_category(
    category: str,
    repository: FundRepository = Depends(get_fund_repository),
) -> list[Fund]:
    """Find all funds in a given asset category.
    Use this to find investment options within a specific asset class,
    for example when building or rebalancing a portfolio.

    Args:
        category: The fund category to filter by (e.g. "Global Equity", "Fixed Income", "Canadian Equity", "Balanced", "Cash Equivalent", "Real Estate"). Case-insensitive.
    """
    return repository.get_by_category(category)


@tools.tool()
async def get_funds_by_risk_level(
    risk_level: str,
    repository: FundRepository = Depends(get_fund_repository),
) -> list[Fund]:
    """Find all funds matching a given risk level.
    Use this to recommend funds that align with a client's risk profile
    or to find lower/higher risk alternatives.

    Args:
        risk_level: The risk level to filter by — "Very Low", "Low", "Low-Medium", "Medium", "Medium-High", "High", or "Very High". Case-insensitive.
    """
    return repository.get_by_risk_level(risk_level)
