from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from agent_framework.foundry import FoundryAgent
from agent_framework import AgentSession, Agent, AgentRunInputs
from dotenv import load_dotenv
import os
import json
import asyncio

async def main():

    load_dotenv(override=True)

    PROJECT_ENDPOINT = os.getenv('PROJECT_ENDPOINT')
    AGENT_NAME = 'WealthAgent'

    project = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=AzureCliCredential()
    )

    # Get the latest version of the agents
    agent_version_details = project.agents.list_versions(agent_name=AGENT_NAME,order='desc')
    agent_definition = next(iter(agent_version_details), None)

    print(agent_definition.version)

    agent = FoundryAgent(
        project_endpoint=PROJECT_ENDPOINT,
        agent_name=AGENT_NAME,
        allow_preview=True,
        agent_version=agent_definition.version,    
        credential=AzureCliCredential(),
    )

    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, 'data', 'multi_turns_conversation.json'), 'r') as f:
        conversations = json.load(f)

    for conversation in conversations:
        print(f"\n--- Conversation: {conversation['name']} ---")
        session = agent.create_session()

        for turn in conversation['turns']:
            query = turn['query']
            print(f"\n--- Query: {query} ---")
            response = await agent.run(query, session=session)
            print(f"\n--- Response: {response.text} ---")
            await asyncio.sleep(2)

asyncio.run(main())            
