"""Specialist agent for mock technical interview sessions."""

from google.adk.agents import Agent
from placement_agent.tools.interview_questions import get_interview_question
from placement_agent.config import INTERVIEW_COACH_SPEC

INTERVIEW_COACH_INSTRUCTION = """
You conduct mock interviews one question at a time.

Supported categories: sde, data, ml, devops, pm, general.

Workflow:
1. Determine the target role category with the user.
2. Fetch the question by calling `get_interview_question(role_category, question_index)`.
3. Present one question at a time. Do not show hints before the user answers.
4. After the user answers, provide concise feedback: what was good, what to improve, key missing points, and a score (1-5).
5. Advance to `question_index + 1` when the user is ready.
"""

interview_coach = Agent(
    name=INTERVIEW_COACH_SPEC.name,
    model=INTERVIEW_COACH_SPEC.model,
    description=INTERVIEW_COACH_SPEC.description,
    instruction=INTERVIEW_COACH_INSTRUCTION,
    tools=[get_interview_question],
)
