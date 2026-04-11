from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.code_executors.container_code_executor import ContainerCodeExecutor

# 2. Configure the LiteLLM Model
model = LiteLlm(model="openai/qwen3-coder:30b",
                api_base="http://localhost:11434/v1", 
                api_key="my_api_key")

root_agent = Agent(
    name="code_assistant",
    model=model,
    code_executor=ContainerCodeExecutor(image="docker-sandbox"),
    instruction="You are a coder. Create Python code to verify your math. if required do pip inst"
)
