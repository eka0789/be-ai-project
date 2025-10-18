from app.services.scoring import cv_weighted_score, project_weighted_score


def test_cv_weighted_score_basic():
    """
    Test the cv_weighted_score function with basic input data.

    Ensures the score is between 0 and 1 and the detail dictionary contains the expected keys.
    """
    cv = {
        "skills": {"python": 1, "fastapi": 1, "docker": 1, "aws": 1, "llm": 1, "rag": 1},
        "years": 3,
        "raw_text": "Led team with strong communication and performance improvements",
    }
    score, detail = cv_weighted_score(cv)
    assert 0 <= score <= 1, f"CV score {score} is not in range [0, 1]"
    assert set(detail.keys()) == {"technical", "experience", "achievements", "culture"}, (
        f"Detail keys {detail.keys()} do not match expected keys"
    )


def test_project_weighted_score_basic():
    """
    Test the project_weighted_score function with basic input data.

    Ensures the score is between 1 and 5 and the detail dictionary contains the expected keys.
    """
    report = {
        "sections": {
            "prompt": 1,
            "chaining": 1,
            "rag": 1,
            "error": 1,
            "retry": 1,
            "testing": 1,
            "deployment": 1,
        }
    }
    score, detail = project_weighted_score(report)
    assert 1 <= score <= 5, f"Project score {score} is not in range [1, 5]"
    assert set(detail.keys()) == {"correctness", "code_quality", "resilience", "docs", "creativity"}, (
        f"Detail keys {detail.keys()} do not match expected keys"
    )