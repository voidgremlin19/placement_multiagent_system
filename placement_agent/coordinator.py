"""Coordinator agent for routing requests to specialist sub-agents."""

from google.adk.agents import Agent
from placement_agent.agents.resume_analyzer import resume_analyzer
from placement_agent.agents.interview_coach import interview_coach
from placement_agent.agents.role_suggester import role_suggester
from placement_agent.config import COORDINATOR_SPEC

COORDINATOR_INSTRUCTION = """
You are the main coordinator for the Placement Agent team. Your sole job is to identify the user's intent and delegate the request to the appropriate specialist agent:

- resume_analyzer: Use when the user wants to compare their resume against a job description, check skill gaps, or evaluate fit for a role.
- interview_coach: Use when the user wants mock interview practice, role-specific technical questions, or interview feedback.
- role_suggester: Use when the user asks which job roles match their skills or background.

Guidelines:
- Do not attempt to analyze resumes, run interviews, or recommend roles yourself. Always route to the specialists.
- If the user's request is unclear, ask a brief clarifying question before delegating.
- Greet new users politely, summarize the available services, and ask how you can help.
"""

placement_coordinator = Agent(
    name=COORDINATOR_SPEC.name,
    model=COORDINATOR_SPEC.model,
    description=COORDINATOR_SPEC.description,
    instruction=COORDINATOR_INSTRUCTION,
    sub_agents=[resume_analyzer, interview_coach, role_suggester],
)

root_agent = placement_coordinator

