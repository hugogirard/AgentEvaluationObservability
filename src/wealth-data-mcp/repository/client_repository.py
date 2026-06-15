import json
from pathlib import Path
from typing import Optional

from models.client import Client
from models.holding import Holding


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

    def add_holding(self, client_id: str, holding: Holding) -> Optional[Client]:
        client = self.get_by_id(client_id)
        if client is None:
            return None
        client.holdings.append(holding)
        self._recalculate(client)
        return client

    def remove_holding(self, client_id: str, fund_code: str) -> Optional[Client]:
        client = self.get_by_id(client_id)
        if client is None:
            return None
        original_len = len(client.holdings)
        client.holdings = [h for h in client.holdings if h.fund_code != fund_code]
        if len(client.holdings) == original_len:
            return None
        self._recalculate(client)
        return client

    def update_holding(
        self,
        client_id: str,
        fund_code: str,
        units: Optional[float] = None,
        market_value: Optional[float] = None,
        book_cost: Optional[float] = None,
    ) -> Optional[Client]:
        client = self.get_by_id(client_id)
        if client is None:
            return None
        holding = next((h for h in client.holdings if h.fund_code == fund_code), None)
        if holding is None:
            return None
        if units is not None:
            holding.units = units
        if market_value is not None:
            holding.market_value = market_value
        if book_cost is not None:
            holding.book_cost = book_cost
        self._recalculate(client)
        return client

    @staticmethod
    def _recalculate(client: Client) -> None:
        total = sum(h.market_value for h in client.holdings)
        client.total_balance = total
        for h in client.holdings:
            h.weight = round((h.market_value / total) * 100, 1) if total > 0 else 0.0
