import pathlib

from google.adk.skills import load_skill_from_dir
from google.adk.tools.skill_toolset import SkillToolset


# ---------------------------------------------------------------------------
# ADK Skills: Modular, progressive disclosure workflows
# ---------------------------------------------------------------------------
skills_root = pathlib.Path(__file__).parent / "skills"

skills = [
    load_skill_from_dir(skills_root / name)
    for name in [
        "abcd-framework-audit",
        "creative-insight-analyzer",
        "daily-briefing",
        "debate-synthesizer",
        "deep-exploration",
        "industry-landscape-briefing",
        "kol-discovery",
        "multi-video-synthesis",
        "poi-discovery-briefing",
        "product-launch-audit",
        "sentiment-analysis",
        "visualization-reporting",
    ]
]

skill_toolset = SkillToolset(skills=skills)


