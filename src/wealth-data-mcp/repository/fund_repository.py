import json
from pathlib import Path
from typing import Optional

from models.fund import Fund

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class FundRepository:
    def __init__(self) -> None:
        with open(DATA_DIR / "funds.json", "r", encoding="utf-8") as f:
            raw = json.load(f)
        self._funds: list[Fund] = [Fund(**item) for item in raw]

    def get_all(self) -> list[Fund]:
        return self._funds

    def get_by_code(self, fund_code: str) -> Optional[Fund]:
        return next((f for f in self._funds if f.fund_code == fund_code), None)

    def get_by_category(self, category: str) -> list[Fund]:
        return [f for f in self._funds if f.category.lower() == category.lower()]

    def get_by_risk_level(self, risk_level: str) -> list[Fund]:
        return [f for f in self._funds if f.risk_level.lower() == risk_level.lower()]
