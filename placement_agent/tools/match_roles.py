"""Tool for scoring candidate skills against static role definitions."""

import json
from pathlib import Path


def _load_role_map() -> dict:
    data_path = Path(__file__).parent.parent / "data" / "role_skill_map.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def match_roles_to_skills(skills: list[str]) -> dict:
    """Matches candidate skills against job role requirements and returns top recommendations."""
    if not skills:
        return {"recommendations": [], "message": "No skills provided."}

    candidate_skills = {s.strip().lower() for s in skills if isinstance(s, str)}
    role_map = _load_role_map()
    scored = []

    for role_name, skill_data in role_map.items():
        required = skill_data.get("required", [])
        preferred = skill_data.get("preferred", [])

        matched_req = [r for r in required if r.lower() in candidate_skills]
        matched_pref = [p for p in preferred if p.lower() in candidate_skills]
        missing_req = [r for r in required if r.lower() not in candidate_skills]

        score_req = len(matched_req) / max(len(required), 1)
        score_pref = len(matched_pref) / max(len(preferred), 1)
        score = (score_req * 0.7) + (score_pref * 0.3)

        if matched_req:
            rationale = f"Strong alignment in {', '.join(matched_req[:4])}."
        else:
            rationale = "Stretch role; consider developing core required skills."

        if missing_req:
            rationale += f" Key missing skills: {', '.join(missing_req[:3])}."

        scored.append({
            "role": role_name,
            "match_score": round(score, 2),
            "matched_skills": matched_req + matched_pref,
            "missing_required": missing_req,
            "rationale": rationale,
        })

    scored.sort(key=lambda x: x["match_score"], reverse=True)

    return {
        "recommendations": scored[:3],
        "skills_analyzed": skills,
    }

