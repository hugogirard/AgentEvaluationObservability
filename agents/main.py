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

    try:
        existing_versions = project.agents.list_versions(agent_name=AGENT_NAME,
                                                        limit=2,
                                                        order='desc')
        previous_versions = [v.version for v in existing_versions]
        previous_versions.reverse()
    except Exception:
        previous_versions = []

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

    # Combine all versions: e.g. "WealthAgent:1,WealthAgent:2"
    all_versions = previous_versions + [agent.version]

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            versions_str = ",".join(f"{AGENT_NAME}:{v}" for v in all_versions)
            f.write(f"AGENT_VERSIONS={versions_str}\n")


if __name__ == "__main__":
    load_dotenv(override=True)
    main()
