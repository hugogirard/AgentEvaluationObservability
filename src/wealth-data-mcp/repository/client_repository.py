import json
from pathlib import Path
from typing import Optional

from models.client import Client
from models.market_summary import MarketSummary
from models.risk_factors import RiskFactors


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class ClientRepository:
    def __init__(self) -> None:
        with open(DATA_DIR / "clients.json", "r", encoding="utf-8") as f:
            raw = json.load(f)
        self._clients: list[Client] = [Client(**item) for item in raw]

    def get_all(self) -> list[Client]:
        return self._clients

    def get_by_id(self, client_id: str) -> Optional[Client]:
        return next((c for c in self._clients if c.client_id == client_id), None)

    def get_by_advisor(self, advisor_id: str) -> list[Client]:
        return [c for c in self._clients if c.advisor_id == advisor_id]

    def get_by_risk_profile(self, risk_profile: str) -> list[Client]:
        return [c for c in self._clients if c.risk_profile.lower() == risk_profile.lower()]
