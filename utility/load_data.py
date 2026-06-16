from azure.cosmos import CosmosClient
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os
import json
import uuid

load_dotenv(override=True)

COSMOS_DB_CONNECTION_STRING = os.getenv('COSMOS_DB_CONNECTION_STRING')
DATABASE_NAME = 'contoso'
CLIENT_CONTAINER = 'client'
FUND_CONTAINER = 'fund'

client = CosmosClient.from_connection_string(COSMOS_DB_CONNECTION_STRING)

db = client.get_database_client(DATABASE_NAME)

client_container = db.get_container_client(CLIENT_CONTAINER)
fund_container = db.get_container_client(FUND_CONTAINER)

for item in client_container.read_all_items():
    client_container.delete_item(item=item['id'], partition_key=item['clientId'])

for item in fund_container.read_all_items():
    fund_container.delete_item(item=item['id'], partition_key=item['fundCode'])

script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, 'data', 'clients.json'), 'r') as f:
    clients = json.load(f)

for client in clients:
   client['id'] = str(uuid.uuid4())
   client_container.create_item(body=client)

with open(os.path.join(script_dir, 'data', 'funds.json'), 'r') as f:
    funds = json.load(f)

for fund in funds:
   fund['id'] = str(uuid.uuid4())
   fund_container.create_item(body=fund)       