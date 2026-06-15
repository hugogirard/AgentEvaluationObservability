from pydantic import BaseModel, Field
from typing import Optional


class Fund(BaseModel):
    model_config = {"populate_by_name": True}

    fund_code: str = Field(alias="fundCode")
    fund_name: str = Field(alias="fundName")
    category: str
    risk_level: str = Field(alias="riskLevel")
    mer: float
    nav_per_unit: Optional[float] = Field(default=None, alias="navPerUnit")
    currency: str
    min_investment: float = Field(alias="minInvestment")
    ytd_return: float = Field(alias="ytdReturn")
    description: str
