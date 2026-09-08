"""Tool for comparing candidate resumes against job descriptions using Gemini."""

import json
import google.genai as genai
from placement_agent.config import MODEL_NAME

_EXTRACTION_PROMPT = """
Analyze the provided RESUME against the JOB DESCRIPTION and return a JSON object with:
- "jd_required_skills": list of required skills in JD
- "jd_preferred_skills": list of preferred skills in JD
- "resume_skills": list of skills in resume
- "overlapping_skills": list of matching skills
- "missing_required_skills": list of missing required skills
- "missing_preferred_skills": list of missing preferred skills
- "match_strength": "strong", "partial", or "weak"
- "verdict": concise assessment and recommendation

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}

Return ONLY raw valid JSON.
"""


def compare_resume_jd(resume_text: str, jd_text: str) -> dict:
    """Extract skills and compare resume against job description using LLM."""
    if not resume_text.strip():
        return {"error": "resume_text cannot be empty."}
    if not jd_text.strip():
        return {"error": "jd_text cannot be empty."}

    prompt = _EXTRACTION_PROMPT.format(
        resume_text=resume_text.strip(),
        jd_text=jd_text.strip(),
    )

    try:
        # No explicit api_key: the SDK auto-detects API-key mode vs. Vertex AI
        # mode from GOOGLE_GENAI_USE_VERTEXAI / GOOGLE_CLOUD_PROJECT /
        # GOOGLE_CLOUD_LOCATION / GOOGLE_API_KEY env vars.
        client = genai.Client()
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        raw = response.text.strip()
        if raw.startswith("```"):
            raw = raw.strip("`").removeprefix("json").strip()
        return json.loads(raw)
    except Exception as e:
        return {"error": f"Failed to compare resume and JD: {e}"}

