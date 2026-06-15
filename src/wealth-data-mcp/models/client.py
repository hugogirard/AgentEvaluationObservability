from pydantic import BaseModel, Field, model_validator
from typing import Optional

from models.holding import Holding


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
    notes: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def extract_notes(cls, data: dict) -> dict:
        if "_notes" in data:
            data["notes"] = data.pop("_notes")
        return data
