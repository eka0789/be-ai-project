from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..utils.db import session_scope
from ..models.job_model import Job


router = APIRouter(prefix="/result", tags=["result"])


@router.get("/{job_id}", response_model=Dict[str, Any])
async def get_job_result(job_id: str) -> Dict[str, Any]:
    """
    Retrieve the status and result of a job by its ID.

    Args:
        job_id: Unique identifier of the job.

    Returns:
        Dictionary containing job ID, status, and either result or error details.

    Raises:
        HTTPException: If the job is not found (404).
        Exception: For other errors during database operations.
    """
    try:
        with session_scope() as s:
            job = s.query(Job).filter(Job.job_id == job_id).first()
            if not job:
                raise HTTPException(status_code=404, detail="Job not found")

            if job.status in ("queued", "processing"):
                return {"id": job.job_id, "status": job.status}
            if job.status == "failed":
                return {"id": job.job_id, "status": job.status, "error": job.error}
            
            return {
                "id": job.job_id,
                "status": job.status,
                "result": job.result_payload,
            }
    except HTTPException:
        raise
    except Exception as e:
        raise Exception(f"Error retrieving job result: {str(e)}")