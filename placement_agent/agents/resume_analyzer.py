"""Specialist agent for evaluating resumes against job descriptions."""

from google.adk.agents import Agent
from placement_agent.tools.compare_resume_jd import compare_resume_jd
from placement_agent.config import RESUME_ANALYZER_SPEC

RESUME_ANALYZER_INSTRUCTION = """
You analyze resumes against job descriptions to provide structured skill gap analysis.

Workflow:
1. Ask the user for their resume text and target job description text if not already provided.
2. Call `compare_resume_jd` with both texts once you have them.
3. Present the analysis clearly, highlighting:
   - Overall match strength (Strong, Partial, or Weak)
   - Overlapping skills
   - Missing required skills
   - Missing preferred skills
   - Qualitative verdict and 1-2 actionable next steps for the candidate.

Always call the `compare_resume_jd` tool rather than doing manual extraction yourself.
"""

resume_analyzer = Agent(
    name=RESUME_ANALYZER_SPEC.name,
    model=RESUME_ANALYZER_SPEC.model,
    description=RESUME_ANALYZER_SPEC.description,
    instruction=RESUME_ANALYZER_INSTRUCTION,
    tools=[compare_resume_jd],
)

