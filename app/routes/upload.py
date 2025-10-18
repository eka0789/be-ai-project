from fastapi import APIRouter, UploadFile, File
from typing import Dict
from ..utils.file_manager import save_upload
from ..utils.db import session_scope
from ..models.document_model import Document


router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("", response_model=Dict[str, str])
async def upload_cv_and_report(cv: UploadFile = File(...), report: UploadFile = File(...)) -> Dict[str, str]:
    """
    Upload CV and report files, save them to storage, and store metadata in the database.

    Args:
        cv: Uploaded CV file.
        report: Uploaded report file.

    Returns:
        Dictionary containing the CV and report document IDs.

    Raises:
        Exception: If file saving or database operations fail.
    """
    try:
        # Save uploaded files
        cv_id, cv_fname, cv_path = save_upload(cv, "cv")
        rep_id, rep_fname, rep_path = save_upload(report, "report")

        # Store document metadata in the database
        with session_scope() as s:
            s.add_all([
                Document(doc_id=cv_id, filename=cv_fname, path=cv_path, kind="cv"),
                Document(doc_id=rep_id, filename=rep_fname, path=rep_path, kind="report"),
            ])
            s.commit()

        return {"cv_id": cv_id, "report_id": rep_id}
    except Exception as e:
        raise Exception(f"Error uploading files or saving to database: {str(e)}")