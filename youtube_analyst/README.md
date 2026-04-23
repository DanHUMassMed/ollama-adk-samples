# YouTube Analyst Agent

## Overview

The YouTube Analyst Agent (**YouBuddy**) is an AI-native "Attention Guardian" and consultative YouTube analysis agent built using the Google ADK framework. Its core philosophy is **Return on Attention (RoA)**, focusing on pre-digesting content and delivering unified, high-density knowledge directly from YouTube. It orchestrates a complex workflow involving data retrieval, text synthesis, sentiment analysis, and interactive visualization.

## Architecture

The application is built on a multi-agent orchestration architecture:

1. **Root Agent (`youtube_agent`)**: The primary coordinator that processes user intents. It is responsible for calling YouTube API tools (like `search_youtube`, `get_video_transcript`, and `get_video_comments`), loading relevant analysis skills dynamically, and orchestrating the final output.
2. **Sub-Agent (`visualization_agent`)**: A specialized agent dedicated to rendering charts and graphs. It generates and executes Plotly or Matplotlib Python code dynamically to provide data visualization artifacts like interactive HTML charts and PNG images.
3. **SkillToolset System**: The agent employs a progressive disclosure skill system. Complex workflows are offloaded into modular skills (e.g., `kol-discovery`, `sentiment-analysis`, `debate-synthesizer`), which the agent can dynamically discover (`list_skills`) and execute (`load_skill`) on-demand.
4. **Local Execution**: The system leverages `LiteLLM` to interface with a locally hosted `gemma4` model via Ollama. It has been configured with a `WebSafeLiteLlm` wrapper to ensure seamless compatibility with the ADK Web UI.

## How to Use

1. **Prerequisites**: 
   - Ensure you have a local Ollama instance running the `gemma4:26b` model. 
   - Set your `YOUTUBE_SEARCH_API` environment variable with a valid YouTube Data API key.

2. **Run the Application**: 
   Start the ADK Web UI by executing the following command in your terminal from the project root:
   ```bash
   uv run adk web youtube_analyst
   ```

3. **Interact**: 
   Open the ADK Web interface in your browser and start chatting with the agent. The agent will "Work Out Loud" to communicate its tool executions and progress to you in real-time. Any generated reports or charts will be exported locally to your `~/Downloads/YouTube-Analyst-Exports/` folder.

## Example Interactions

- **Trend Analysis:** "Find the top 5 videos about 'Generative AI' from the last month and plot their view counts."
- **Competitor Research:** "Compare the engagement rates of MKBHD and Linus Tech Tips."
- **Audience Feedback:** "What is the sentiment of the comments on the latest OpenAI video? Summarize the top concerns."
- **Visual Reporting:** "Create a bar chart comparing the subscriber counts of the top 3 tech reviewers."

## Original Authors

- Pili Hu
- Jasmine Tong
- Kun Wang
- Jeff Yang
