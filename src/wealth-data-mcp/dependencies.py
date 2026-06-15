from contextlib import asynccontextmanager
from repository import ClientRepository, FundRepository


@asynccontextmanager
async def get_client_repository():
    client_repository = ClientRepository()
    try:
        yield client_repository
    finally:
        pass

@asynccontextmanager
async def get_fund_repository():
    fund_repository = FundRepository()
    try:
        yield fund_repository
    finally:
        pass