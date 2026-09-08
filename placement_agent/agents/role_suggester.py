"""Specialist agent for recommending target job roles based on skills."""

from google.adk.agents import Agent
from placement_agent.tools.match_roles import match_roles_to_skills
from placement_agent.config import ROLE_SUGGESTER_SPEC

ROLE_SUGGESTER_INSTRUCTION = """
You recommend the best-fit job roles based on candidate skills.

Workflow:
1. Ask the user for their skills if not provided or extracted from previous steps.
2. Call `match_roles_to_skills(skills)` with a list of skill strings.
3. Present the top 3 recommended roles with match scores, matching skills, skill gaps, and 1-2 actionable tips to bridge those gaps.

Always use `match_roles_to_skills` to compute recommendations.
"""

role_suggester = Agent(
    name=ROLE_SUGGESTER_SPEC.name,
    model=ROLE_SUGGESTER_SPEC.model,
    description=ROLE_SUGGESTER_SPEC.description,
    instruction=ROLE_SUGGESTER_INSTRUCTION,
    tools=[match_roles_to_skills],
)

