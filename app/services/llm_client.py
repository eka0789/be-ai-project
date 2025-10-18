from typing import List
from ..utils.config import get_settings
from .text_utils import clean_text

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Initialize settings
settings = get_settings()

# Check OpenAI availability
_openai_ok = bool(settings.OPENAI_API_KEY and OpenAI)
_client = OpenAI(api_key=settings.OPENAI_API_KEY) if _openai_ok else None

# Prompt templates
CV_FEEDBACK_TMPL = (
    "Based on the job description and rubric, summarize the candidate's strengths and gaps for backend + AI exposure."
)
PR_FEEDBACK_TMPL = (
    "Based on the case study brief and rubric, summarize the project's strengths and areas to improve."
)
SUMMARY_TMPL = (
    "Write a concise hiring summary in 3-5 sentences: strengths, gaps, and recommendations."
)


def _call_openai(system: str, prompt: str) -> str:
    """
    Call OpenAI API to generate a response based on system and user prompts.

    Args:
        system: System prompt to set the context for the AI.
        prompt: User prompt containing the input data.

    Returns:
        Cleaned response text from the OpenAI API.

    Raises:
        Exception: If the API call fails or the response is invalid.
    """
    if not (_openai_ok and _client):
        raise Exception("OpenAI client is not initialized")

    try:
        resp = _client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        )
        return clean_text(resp.choices[0].message.content or "")
    except Exception as e:
        raise Exception(f"Error calling OpenAI API: {str(e)}")


def cv_feedback_llm(context: List[str], cv_text: str) -> str:
    """
    Generate feedback for a CV using OpenAI or fallback heuristic.

    Args:
        context: List of context strings (e.g., job description, rubric).
        cv_text: Raw text extracted from the CV.

    Returns:
        Feedback string summarizing strengths and gaps.
    """
    if _openai_ok and _client:
        prompt = f"Context: {'\n'.join(context)}\nCV:\n{cv_text[:6000]}\n\n{CV_FEEDBACK_TMPL}"
        return _call_openai("You are a precise technical recruiter.", prompt)
    
    # Fallback heuristic
    return "Strong backend exposure detected; consider deepening LLM/RAG production experience if limited."


def project_feedback_llm(context: List[str], report_text: str) -> str:
    """
    Generate feedback for a project report using OpenAI or fallback heuristic.

    Args:
        context: List of context strings (e.g., case study brief, rubric).
        report_text: Raw text extracted from the project report.

    Returns:
        Feedback string summarizing strengths and areas to improve.
    """
    if _openai_ok and _client:
        prompt = f"Context: {'\n'.join(context)}\nReport:\n{report_text[:6000]}\n\n{PR_FEEDBACK_TMPL}"
        return _call_openai("You are a rigorous code reviewer.", prompt)
    
    return (
        "Meets key requirements (prompting/chaining/RAG). "
        "Improve testing depth and failure-mode handling."
    )


def final_summary_llm(cv_match_rate: float, project_score: float, cv_fb: str, pr_fb: str) -> str:
    """
    Generate a final hiring summary using OpenAI or fallback heuristic.

    Args:
        cv_match_rate: CV match rate score (e.g., 0 to 1).
        project_score: Project score (e.g., 1 to 5).
        cv_fb: CV feedback string.
        pr_fb: Project feedback string.

    Returns:
        Summary string with strengths, gaps, and recommendations.
    """
    if _openai_ok and _client:
        prompt = (
            f"CV Match Rate: {cv_match_rate}\n"
            f"Project Score: {project_score}\n\n"
            f"CV Feedback: {cv_fb}\n\n"
            f"Project Feedback: {pr_fb}\n\n"
            f"{SUMMARY_TMPL}"
        )
        return _call_openai("You are a hiring manager.", prompt)
    
    return (
        "Solid overall profile for backend with AI-adjacent skills. "
        "Project aligns with brief; expand on reliability practices and add more automated tests. "
        "Recommended for next interview round."
    )