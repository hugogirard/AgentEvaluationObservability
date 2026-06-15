from pydantic import BaseModel, Field


class AssetAllocation(BaseModel):
    model_config = {"populate_by_name": True}

    canadian_equities: float = Field(alias="canadianEquities")
    us_equities: float = Field(alias="usEquities")
    international_equities: float = Field(alias="internationalEquities")
    canadian_bonds: float = Field(alias="canadianBonds")
    corporate_bonds: float = Field(alias="corporateBonds")
    cash_equivalents: float = Field(alias="cashEquivalents")
