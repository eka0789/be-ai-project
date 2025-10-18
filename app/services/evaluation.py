from typing import Dict
from .cv_parser import parse_cv
from .project_parser import parse_report
from .rag_retriever import retrieve_context
from .scoring import cv_weighted_score, project_weighted_score
from .llm_client import cv_feedback_llm, project_feedback_llm, final_summary_llm


def evaluate(cv_path: str, report_path: str, job_title: str) -> Dict[str, any]:
    """
    Evaluate a candidate's CV and project report for a given job title.

    Args:
        cv_path: Path to the CV PDF file.
        report_path: Path to the project report PDF file.
        job_title: Job title to contextualize the evaluation.

    Returns:
        Dictionary containing CV match rate, CV details, CV feedback, project score,
        project details, project feedback, and overall summary.

    Raises:
        FileNotFoundError: If CV or report file does not exist.
        Exception: For other errors during evaluation.
    """
    try:
        # Parse documents
        cv_data = parse_cv(cv_path)
        report_data = parse_report(report_path)

        # Retrieve contexts
        jd_ctx = retrieve_context("job_desc", f"{job_title} backend requirements")
        cv_rubric_ctx = retrieve_context("cv_rubric", "cv scoring rubric for backend")
        brief_ctx = retrieve_context("case_brief", "case study backend ai rag")
        pr_rubric_ctx = retrieve_context("project_rubric", "project scoring rubric")

        # Calculate scores
        cv_match_rate, cv_detail = cv_weighted_score(cv_data)
        project_score, pr_detail = project_weighted_score(report_data)

        # Generate LLM feedback
        cv_feedback = cv_feedback_llm(jd_ctx + cv_rubric_ctx, cv_data["raw_text"])
        project_feedback = project_feedback_llm(brief_ctx + pr_rubric_ctx, report_data["raw_text"])

        # Generate final summary
        summary = final_summary_llm(cv_match_rate, project_score, cv_feedback, project_feedback)

        return {
            "cv_match_rate": cv_match_rate,
            "cv_detail": cv_detail,
            "cv_feedback": cv_feedback,
            "project_score": project_score,
            "project_detail": pr_detail,
            "project_feedback": project_feedback,
            "overall_summary": summary,
        }
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error accessing file: {str(e)}")
    except Exception as e:
        raise Exception(f"Error during evaluation: {str(e)}")