from contextlib import asynccontextmanager
from repository import ClientRepository, FundRepository
from azure.cosmos.aio import CosmosClient
from dotenv import load_dotenv
import os

load_dotenv(override=True)

client = CosmosClient.from_connection_string(os.getenv('COSMOS_DB_CONNECTION_STRING'))

COSMOS_DB_CONNECTION_STRING = os.getenv('COSMOS_DB_CONNECTION_STRING')
if not COSMOS_DB_CONNECTION_STRING:
    raise RuntimeError("COSMOS_DB_CONNECTION_STRING environment variable is not set")

db = client.get_database_client('contoso')
container_client = db.get_container_client('client')

@asynccontextmanager
async def get_client_repository():
    client_repository = ClientRepository(container=container_client)
    try:
        yield client_repository
    finally:
        pass

# @asynccontextmanager
# async def get_fund_repository():
#     fund_repository = FundRepository()
#     try:
#         yield fund_repository
#     finally:
#         pass