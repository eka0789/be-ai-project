import traceback
from typing import Dict
from .utils.queue import celery_app
from .utils.logger import logger
from .services.evaluation import evaluate
from .utils.db import session_scope
from .models.job_model import Job


@celery_app.task(
    name="app.tasks.evaluate_job",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def evaluate_job(job_id: str, payload: Dict[str, str]) -> None:
    """
    Celery task to evaluate a job application by processing CV and report.

    Args:
        job_id: Unique identifier for the job.
        payload: Dictionary containing 'cv_path', 'report_path', and 'job_title'.

    Raises:
        Exception: If evaluation fails, with error details logged and stored in the job record.
    """
    logger.info(f"[JOB {job_id}] Starting evaluation")
    
    try:
        with session_scope() as s:
            job = s.query(Job).filter(Job.job_id == job_id).one()
            job.status = "processing"
            s.flush()

        result = evaluate(payload["cv_path"], payload["report_path"], payload["job_title"])

        with session_scope() as s:
            job = s.query(Job).filter(Job.job_id == job_id).one()
            job.status = "completed"
            job.result_payload = result
            s.flush()

        logger.info(f"[JOB {job_id}] Completed successfully")
    
    except Exception as e:
        logger.error(f"[JOB {job_id}] Failed: {str(e)}\n{traceback.format_exc()}")
        with session_scope() as s:
            job = s.query(Job).filter(Job.job_id == job_id).one()
            job.status = "failed"
            job.error = str(e)
            s.flush()
        raise