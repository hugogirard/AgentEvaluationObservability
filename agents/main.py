from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from azure.ai.projects.models import PromptAgentDefinition, Connection, MCPTool
from dotenv import load_dotenv
import os

def main():

    PROJECT_ENDPOINT = os.getenv('PROJECT_ENDPOINT')
    AGENT_MODEL = os.getenv("AGENT_MODEL")
    AGENT_NAME = 'WealthAgent'
    MCP_CONNECTION_NAME =  'WEALTH-MCP-SERVER'

    project = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=AzureCliCredential(),
    )

    connections = project.connections.list(connection_type='RemoteTool')
    mcp_connection: Connection = None

    for connection in connections:
        if connection.name == MCP_CONNECTION_NAME:
            mcp_connection = connection
            print(mcp_connection.__dict__)
            break
    
    if mcp_connection is None:
        raise Exception('MCP connection not found')

    tool = MCPTool(
        server_label=mcp_connection.name,
        server_url=mcp_connection.target,
        require_approval='never',
        project_connection_id=mcp_connection.name
    )

    with open('prompt.txt', 'r', encoding='utf-8') as file:
        prompt = file.read()

    agent = project.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=AGENT_MODEL,
            instructions=prompt,
            tools=[tool]
        ),
    )        
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")


if __name__ == "__main__":
    load_dotenv(override=True)
    main()
