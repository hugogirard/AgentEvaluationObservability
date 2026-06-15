from pydantic import BaseModel, Field, model_validator
from typing import Optional

from models.holding import Holding
from models.asset_allocation import AssetAllocation


class Client(BaseModel):
    model_config = {"populate_by_name": True}

    id: str
    client_id: str = Field(alias="clientId")
    name: str
    risk_profile: str = Field(alias="riskProfile")
    account_type: str = Field(alias="accountType")
    advisor_id: str = Field(alias="advisorId")
    last_review_date: str = Field(alias="lastReviewDate")
    total_balance: float = Field(alias="totalBalance")
    holdings: list[Holding]
    asset_allocation: AssetAllocation = Field(alias="assetAllocation")
    total_equity_percent: float = Field(alias="totalEquityPercent")
    total_fixed_income_percent: float = Field(alias="totalFixedIncomePercent")
    notes: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def extract_notes(cls, data: dict) -> dict:
        if "_notes" in data:
            data["notes"] = data.pop("_notes")
        return data
