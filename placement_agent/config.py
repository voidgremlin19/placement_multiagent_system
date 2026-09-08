"""Central configuration for the Placement Agent system.

Single source of truth for the model every agent runs on, plus each
agent's identity spec (name/description). No other file should hardcode
a model string or an agent's name/description literal.
"""

from dataclasses import dataclass

# The only model used across the entire agent system.
#
# NOTE on model choice (verified directly against the Gemini API for this
# account on 2026-09-07):
#   - gemini-2.5-flash / gemini-2.5-flash-lite: 404, "no longer available
#     to new users" -- the whole 2.5 generation is blocked, no fix exists.
#   - gemini-3.6-flash (flagship): works, but free tier is capped at just
#     20 requests/day for this account -- exhausted almost immediately
#     during normal dev testing.
#   - gemini-flash-lite-latest: works, and the free tier's lite-model
#     quota is meaningfully higher than the flagship's. This is a
#     Google-maintained alias that always points at the current lite
#     model, so it won't dead-end into a 404 the way a pinned model name
#     eventually will.
MODEL_NAME = "gemini-flash-lite-latest"


@dataclass(frozen=True)
class AgentSpec:
    name: str
    description: str
    model: str = MODEL_NAME


COORDINATOR_SPEC = AgentSpec(
    name="placement_coordinator",
    description="Main router agent for placement assistance.",
)

RESUME_ANALYZER_SPEC = AgentSpec(
    name="resume_analyzer",
    description="Compares resume text with job descriptions to surface skill gaps and match strength.",
)

INTERVIEW_COACH_SPEC = AgentSpec(
    name="interview_coach",
    description="Runs role-specific mock interview practice sessions.",
)

ROLE_SUGGESTER_SPEC = AgentSpec(
    name="role_suggester",
    description="Suggests job roles based on technical skills and experience.",
)
