"""Tool for stepping through the mock-interview question bank."""

import json
from pathlib import Path


def _load_question_bank() -> dict:
    data_path = Path(__file__).parent.parent / "data" / "interview_question_bank.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_interview_question(role_category: str, question_index: int) -> dict:
    """Fetch an interview question from the bank by role category and index."""
    bank = _load_question_bank()
    category = role_category.lower().strip()

    if category not in bank:
        return {
            "error": f"Unknown category '{role_category}'. Available: {list(bank.keys())}",
            "is_complete": False,
        }

    questions = bank[category]["questions"]
    label = bank[category]["label"]
    total = len(questions)

    if question_index >= total:
        return {
            "is_complete": True,
            "category_label": label,
            "total_questions": total,
            "message": f"Completed all {total} questions for {label}.",
        }

    q = questions[question_index]
    return {
        "question": q["question"],
        "hints": q["hints"],
        "good_answer_keywords": q.get("good_answer_keywords", []),
        "category_label": label,
        "question_index": question_index,
        "total_questions": total,
        "is_complete": False,
    }
