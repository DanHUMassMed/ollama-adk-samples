from google.adk import Agent
from .skills import skill_toolset
from .config import config

root_agent = Agent(
    model=config.BASE_MODEL,
    name="blog_skills_agent",
    description="A blog-writing agent powered by reusable skills.",
    instruction=(
        "You are a blog-writing assistant with specialized skills.\n\n"
        "You have four skills available:\n"
        "- **seo-checklist**: SEO optimization rules (load for SEO review)\n"
        "- **blog-writer**: Writing structure and style guide (load for writing)\n"
        "- **content-research-writer**: Research methodology (load for research)\n"
        "- **skill-creator**: Generate new skill definitions (load to create skills)\n\n"
        "When the user asks you to write, research, or optimize a blog post:\n"
        "1. Load the relevant skill(s) to get detailed instructions\n"
        "2. Use `load_skill_resource` to access reference materials\n"
        "3. Follow the skill's step-by-step instructions\n"
        "4. Apply multiple skills together when appropriate\n\n"
        "When the user asks you to create a new skill:\n"
        "1. Load the skill-creator skill\n"
        "2. Read the specification and example references\n"
        "3. Generate a complete SKILL.md that follows the spec\n\n"
        "Always explain which skill you're using and why."
    ),
    tools=[skill_toolset],
)