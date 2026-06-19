
from dotenv import load_dotenv
import os


load_dotenv(override=True)

model_deployment = os.environ["AGENT_MODEL"]

continuous_testing_criteria = [
    # RAG evaluators
    {"type": "azure_ai_evaluator", "name": "groundedness", "evaluator_name": "builtin.groundedness",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}},
    {"type": "azure_ai_evaluator", "name": "relevance", "evaluator_name": "builtin.relevance",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}},
    # General purpose evaluators
    {"type": "azure_ai_evaluator", "name": "fluency", "evaluator_name": "builtin.fluency",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"response": "{{item.response}}"}},
    {"type": "azure_ai_evaluator", "name": "coherence", "evaluator_name": "builtin.coherence",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}},
    # Agent system evaluators
    {"type": "azure_ai_evaluator", "name": "task_completion", "evaluator_name": "builtin.task_completion",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}},
    {"type": "azure_ai_evaluator", "name": "task_adherence", "evaluator_name": "builtin.task_adherence",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}},
    {"type": "azure_ai_evaluator", "name": "intent_resolution", "evaluator_name": "builtin.intent_resolution",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}"}},
    # Agent process evaluators (tool-related)
    {"type": "azure_ai_evaluator", "name": "tool_selection", "evaluator_name": "builtin.tool_selection",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}", "tool_definitions": "{{item.tool_definitions}}"}},
    {"type": "azure_ai_evaluator", "name": "tool_input_accuracy", "evaluator_name": "builtin.tool_input_accuracy",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}", "tool_definitions": "{{item.tool_definitions}}"}},
    {"type": "azure_ai_evaluator", "name": "tool_output_utilization", "evaluator_name": "builtin.tool_output_utilization",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}", "tool_definitions": "{{item.tool_definitions}}"}},
    {"type": "azure_ai_evaluator", "name": "tool_call_success", "evaluator_name": "builtin.tool_call_success",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"response": "{{item.response}}"}},
    {"type": "azure_ai_evaluator", "name": "tool_call_accuracy", "evaluator_name": "builtin.tool_call_accuracy",
     "initialization_parameters": {"deployment_name": model_deployment},
     "data_mapping": {"query": "{{item.query}}", "response": "{{item.response}}", "tool_definitions": "{{item.tool_definitions}}"}},
]