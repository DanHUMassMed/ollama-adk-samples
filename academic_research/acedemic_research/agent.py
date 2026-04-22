from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from .config import config
from .callbacks import intercept_and_parse_pdf
from . import prompt
from .sub_agents.academic_newresearch import academic_newresearch_agent
from .sub_agents.academic_websearch import academic_websearch_agent


academic_coordinator = LlmAgent(
    name="academic_coordinator",
    model=config.BASE_MODEL,
    description=(
        "analyzing seminal papers provided by the users, "
        "providing research advice, locating current papers "
        "relevant to the seminal paper, generating suggestions "
        "for new research directions, and accessing web resources "
        "to acquire knowledge"
    ),
    instruction=prompt.ACADEMIC_COORDINATOR_PROMPT,
    output_key="seminal_paper",
    tools=[
        AgentTool(agent=academic_websearch_agent),
        AgentTool(agent=academic_newresearch_agent),
    ],
    before_model_callback=intercept_and_parse_pdf,
)

root_agent = academic_coordinator
