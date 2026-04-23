# Agent Skills Tutorial

This tutorial demonstrates how to enhance a Google ADK agent with reusable **Skills**. It serves as an introductory guide to the `SkillToolset`, showcasing how to modularize agent instructions, load external tools dynamically, and even create new skills on the fly.

> **Note:** This tutorial is configured to run locally using the **gemma4:26b** model via Ollama.

## Overview

In traditional LLM agent development, system prompts often grow massive and unwieldy as you try to teach the agent every possible task it might need to perform. The **Skills** pattern solves this by keeping the base agent simple and providing it with a library of "skills" it can load on demand.

This project implements a **Blog Skills Agent** (`blog_skills_agent`) equipped with four distinct types of skills to handle blog writing, SEO optimization, content research, and skill creation.

## Architecture

The architecture revolves around the `SkillToolset` provided by Google ADK. When attached to an agent, this toolset automatically gives the agent the ability to:
1. `list_skills` - See what skills are available.
2. `load_skill` - Load the detailed instructions and tools for a specific skill.
3. `load_skill_resource` - Read reference materials associated with a skill.

### The Four Skill Patterns

The codebase (`agent_skills_tutorial/skills.py`) demonstrates four distinct ways to define and load skills:

1. **Inline Skill (`seo-checklist`)**
   - **How it works:** Defined directly in Python code.
   - **Best for:** Simple, static rules that don't require external files or resources.
   - **Usage:** Provides quick SEO rules (title tags, meta descriptions, etc.)

2. **File-Based Skill (`blog-writer`)**
   - **How it works:** Loaded from a local directory containing a `SKILL.md` file.
   - **Best for:** Complex skills with large instruction sets, reference docs, or templates.
   - **Usage:** Provides structured writing guidelines.

3. **External Skill (`content-research-writer`)**
   - **How it works:** Loaded from a directory, simulating a cloned/downloaded community repository.
   - **Best for:** Sharing standards across an organization or pulling in third-party capabilities.
   - **Usage:** Provides research methodologies.

4. **Meta Skill (`skill-creator`)**
   - **How it works:** A skill designed to generate new ADK-compatible skills.
   - **Best for:** Self-extending agents that can expand their own capabilities.
   - **Usage:** The agent reads the `skill-spec.md` and generates a new `SKILL.md` when the user asks for a new capability.

These are bundled into a `SkillToolset` and passed to the `Agent` in `agent.py`. The models are configured to connect to your local Ollama instance running `gemma4:26b` via LiteLLM (`config.py`).

## Running the Agent

You can run this agent using the ADK Web interface:

```bash
uv run adk web agent_skills_tutorial
```

## Example Usages

Test these queries in the ADK Web interface to see the agent dynamically loading and applying its skills:

| # | Query | What It Demonstrates |
|---|-------|---------------------|
| 1 | "I have a blog post titled 'Getting Started with Kubernetes'. Can you review it for SEO?" | **Inline skill** (`seo-checklist`) loaded on demand. |
| 2 | "Help me write a short introduction for a blog about Python async programming. Make it SEO-friendly." | **Multi-skill orchestration**: The agent loads `blog-writer` + `seo-checklist` in parallel to complete the task. |
| 3 | "Can you use your video-editing skill to create a thumbnail?" | **Edge case**: The agent checks its available skills, realizes it lacks video-editing capabilities, and handles the request gracefully. |
| 4 | "OK, then use your content research skill to help me research async Python" | **External skill** (`content-research-writer`) showcasing how the agent can pull in heavier external logic. |
| 5 | "I need a new skill for reviewing Python code for security vulnerabilities. Can you create a SKILL.md?" | **Meta skill**: The `skill-creator` is loaded, enabling the agent to act as a developer and generate a new skill definition based on the spec. |
