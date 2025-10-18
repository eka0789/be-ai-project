from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from typing import Dict
from ..utils.db import session_scope
from ..models.document_model import Document
from ..models.job_model import Job
from ..tasks.evaluate_job import evaluate_job


router = APIRouter(prefix="/evaluate", tags=["evaluate"])


class EvalReq(BaseModel):
    """Request model for evaluation endpoint."""
    job_title: str
    cv_id: str
    report_id: str


@router.post("", response_model=Dict[str, str])
async def evaluate_application(req: EvalReq) -> Dict[str, str]:
    """
    Enqueue a job to evaluate a CV and report for a given job title.

    Args:
        req: Request containing job title, CV ID, and report ID.

    Returns:
        Dictionary with job ID and status ("queued").

    Raises:
        HTTPException: If CV or report document is not found (404).
        Exception: For other errors during database operations or task queuing.
    """
    try:
        with session_scope() as s:
            # Validate document existence
            cv = s.query(Document).filter(Document.doc_id == req.cv_id).first()
            report = s.query(Document).filter(Document.doc_id == req.report_id).first()
            if not cv or not report:
                raise HTTPException(status_code=404, detail="Document not found")

            # Create job
            job_id = f"job_{uuid.uuid4().hex[:8]}"
            payload = {
                "cv_path": cv.path,
                "report_path": report.path,
                "job_title": req.job_title,
            }
            job = Job(job_id=job_id, status="queued", request_payload=payload)
            s.add(job)
            s.commit()  # Explicit commit to ensure job is saved before task

            # Enqueue background task
            evaluate_job.delay(job_id, payload)

            return {"id": job_id, "status": "queued"}
    except HTTPException:
        raise
    except Exception as e:
        raise Exception(f"Error initiating evaluation: {str(e)}")