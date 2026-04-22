
"""Academic_newresearch_agent for finding new research lines"""

from google.adk import Agent
from . import prompt
from ...config import config

academic_newresearch_agent = Agent(
    model=config.BASE_MODEL,
    name="academic_newresearch_agent",
    instruction=prompt.ACADEMIC_NEWRESEARCH_PROMPT,
)
