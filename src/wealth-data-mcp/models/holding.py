from pydantic import BaseModel, Field


class Holding(BaseModel):
    model_config = {"populate_by_name": True}

    fund_code: str = Field(alias="fundCode")
    fund_name: str = Field(alias="fundName")
    units: float
    market_value: float = Field(alias="marketValue")
    book_cost: float = Field(alias="bookCost")
    weight: float
