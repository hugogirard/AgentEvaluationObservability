from pathlib import Path
from typing import Optional
from azure.cosmos.aio import ContainerProxy
from models.client import Client
from models.holding import Holding
import json

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class ClientRepository:
    def __init__(self,container: ContainerProxy) -> None:
        self._container = container

    async def get_all(self) -> list[Client]:
        return [item async for item in self._container.read_all_items()]

    async def get_by_id(self, client_id: str) -> Optional[Client]:
        query = "SELECT * FROM c WHERE c.clientId = @clientId"
        parameters = [{"name": "@clientId", "value": client_id}]
        items = [item async for item in self._container.query_items(query=query, parameters=parameters)]
        return items[0] if items else None

    async def get_by_advisor(self, advisor_id: str) -> list[Client]:
        query = "SELECT * FROM c WHERE c.advisorId = @advisorId"
        parameters = [{"name": "@advisorId", "value": advisor_id}]
        return [item async for item in self._container.query_items(query=query, parameters=parameters)]

    async def get_by_risk_profile(self, risk_profile: str) -> list[Client]:
        query = "SELECT * FROM c WHERE c.riskProfile = @riskProfile"
        parameters = [{"name": "@riskProfile", "value": risk_profile}]
        return [item async for item in self._container.query_items(query=query, parameters=parameters)]

    # def add_holding(self, client_id: str, holding: Holding) -> Optional[Client]:
    #     client = self.get_by_id(client_id)
    #     if client is None:
    #         return None
    #     client.holdings.append(holding)
    #     self._recalculate(client)
    #     return client

    # def remove_holding(self, client_id: str, fund_code: str) -> Optional[Client]:
    #     client = self.get_by_id(client_id)
    #     if client is None:
    #         return None
    #     original_len = len(client.holdings)
    #     client.holdings = [h for h in client.holdings if h.fund_code != fund_code]
    #     if len(client.holdings) == original_len:
    #         return None
    #     self._recalculate(client)
    #     return client

    # def update_holding(
    #     self,
    #     client_id: str,
    #     fund_code: str,
    #     units: Optional[float] = None,
    #     market_value: Optional[float] = None,
    #     book_cost: Optional[float] = None,
    # ) -> Optional[Client]:
    #     client = self.get_by_id(client_id)
    #     if client is None:
    #         return None
    #     holding = next((h for h in client.holdings if h.fund_code == fund_code), None)
    #     if holding is None:
    #         return None
    #     if units is not None:
    #         holding.units = units
    #     if market_value is not None:
    #         holding.market_value = market_value
    #     if book_cost is not None:
    #         holding.book_cost = book_cost
    #     self._recalculate(client)
    #     return client

    # @staticmethod
    # def _recalculate(client: Client) -> None:
    #     total = sum(h.market_value for h in client.holdings)
    #     client.total_balance = total
    #     for h in client.holdings:
    #         h.weight = round((h.market_value / total) * 100, 1) if total > 0 else 0.0
