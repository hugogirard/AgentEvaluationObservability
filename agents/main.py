from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from azure.ai.projects.models import (
    PromptAgentDefinition, 
    Connection, 
    MCPTool,
    EvaluationRule,
    ContinuousEvaluationRuleAction,    
    EvaluationRuleFilter,
    EvaluationRuleEventType
)
from evaluations import continuous_testing_criteria
from dotenv import load_dotenv
from datetime import datetime, timezone
import os

def schedule_evaluation(project: AIProjectClient, agent_name:str):
    
    EVALUATION_NAME = 'continuous_evaluation_wealthagent_users'

    try:
        evaluation = project.evaluation_rules.get(id=EVALUATION_NAME)
    except:
        evaluation = None        

    if evaluation:
        print('Continuous evaluation already present, no need to create it again')
        return
    else:
        print(f'Continuous evaluation not present, creating {EVALUATION_NAME}')

    # Uncomment this in case some errors occurs
    #project.evaluation_rules.delete('continuous_evaluation_wealthagent_users')

    openai_client = project.get_openai_client()

    # We set the datasource to be the response from the openai client
    data_source_config = {"type": "azure_ai_source", "scenario": "responses"}

    eval_object = openai_client.evals.create(
        name=f"Continuous Evaluation {agent_name}",
        data_source_config=data_source_config,
        testing_criteria=continuous_testing_criteria,
    )

    print(f"Evaluation created (id: {eval_object.id}, name: {eval_object.name})")

    continuous_eval_rule = project.evaluation_rules.create_or_update(
        id=EVALUATION_NAME,
        evaluation_rule=EvaluationRule(
            display_name=f"Continuous evaluation for agent {agent_name}",
            description=f"An eval rule that runs for agent {agent_name} response completions",
            action=ContinuousEvaluationRuleAction(eval_id=eval_object.id, max_hourly_runs=10), # Sampling rate not available in the SDK, to change use the portal
            event_type=EvaluationRuleEventType.RESPONSE_COMPLETED,
            filter=EvaluationRuleFilter(agent_name=agent_name),
            enabled=True,
        ),
    )

    print(
        f"Continuous Evaluation Rule created (id: {continuous_eval_rule.id}, name: {continuous_eval_rule.display_name})"
    )    

def main():

    PROJECT_ENDPOINT = os.getenv('PROJECT_ENDPOINT')
    AGENT_MODEL = os.getenv("AGENT_MODEL")
    AGENT_NAME = 'WealthAgent'
    MCP_CONNECTION_NAME =  'WEALTH-MCP-SERVER'
    LIMIT_VERSION_RETRIEVAL = 1 # This will factor how many version we compare behind for the evaluation
                                # in this case always 1 only

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
                                                        order='desc')
        previous_versions = [v.version for v in existing_versions][:LIMIT_VERSION_RETRIEVAL]
        previous_versions.reverse()
    except Exception:
        previous_versions = []

    with open('prompt.txt', 'r', encoding='utf-8') as file:
        prompt = file.read()

    build_timestamp = datetime.now(timezone.utc).isoformat()

    agent = project.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=AGENT_MODEL,
            instructions=prompt,
            tools=[tool]
        ),
        description="Wealth-advisory assistant that helps financial advisors manage client portfolios and explore the bank's fund catalog.",
        metadata={"built_on": build_timestamp},
    )        
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # Combine all versions: e.g. "WealthAgent:1,WealthAgent:2"
    all_versions = previous_versions + [agent.version]
    
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            versions_str = ",".join(f"{AGENT_NAME}:{v}" for v in all_versions)
            f.write(f"AGENT_VERSIONS={versions_str}\n")

    schedule_evaluation(project=project,agent_name=AGENT_NAME)
    
if __name__ == "__main__":
    load_dotenv(override=True)
    main()
