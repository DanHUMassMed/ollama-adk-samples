from google import genai
from google.adk.agents import Agent

from .config import config
from .prompt import YOUTUBE_AGENT_PROMPT
from .skills import skill_toolset
from .tools import (
    aggregate_comment_sentiment,
    analyze_sentiment_heuristic,
    calculate_engagement_metrics,
    calculate_match_score,
    generate_timestamp_url,
    get_channel_details,
    get_comment_replies,
    get_current_date_time,
    get_date_range,
    get_trending_videos,
    get_video_comments,
    get_video_details,
    get_video_transcript,
    publish_file,
    render_html,
    search_channel_videos,
    search_youtube,
    submit_feedback,
)
from .sub_agents.visualization.agent import visualization_agent


youtube_agent = Agent(
    model=config.BASE_MODEL,
    name="youtube_agent",
    description="Agent for YouTube analysis and data retrieval",
    instruction=YOUTUBE_AGENT_PROMPT,
    sub_agents=[visualization_agent],
    tools=[
        search_youtube,
        get_trending_videos,
        get_video_details,
        get_channel_details,
        search_channel_videos,
        get_video_comments,
        get_comment_replies,
        aggregate_comment_sentiment,
        get_video_transcript,
        generate_timestamp_url,
        calculate_engagement_metrics,
        calculate_match_score,
        analyze_sentiment_heuristic,
        get_current_date_time,
        get_date_range,
        submit_feedback,
        render_html,
        publish_file,
        skill_toolset,  # Registers list_skills, load_skill, load_skill_resource
    ],
    generate_content_config=genai.types.GenerateContentConfig(
        max_output_tokens=config.YOUTUBE_AGENT_MAX_OUTPUT_TOKENS,
    ),
)

root_agent = youtube_agent
