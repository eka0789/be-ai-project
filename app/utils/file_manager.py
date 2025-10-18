import os
import uuid
from typing import Tuple
from .config import get_settings


# Initialize settings
settings = get_settings()

# Create upload directory
UPLOAD_DIR = os.path.join(settings.STORAGE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create internal directory (for future use or other operations)
INTERNAL_DIR = os.path.join(settings.STORAGE_DIR, "internal")
os.makedirs(INTERNAL_DIR, exist_ok=True)


def save_upload(file, kind: str) -> Tuple[str, str, str]:
    """
    Save an uploaded file to the storage directory and return its ID, filename, and path.

    Args:
        file: The uploaded file object (e.g., FastAPI UploadFile).
        kind: The type of document (e.g., "cv", "report", "internal").

    Returns:
        Tuple of (doc_id: str, filename: str, path: str).

    Raises:
        IOError: If file writing fails.
    """
    ext = os.path.splitext(file.filename)[1]
    doc_id = f"{kind}_{uuid.uuid4().hex[:8]}"
    filename = f"{doc_id}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(file.file.read())

    return doc_id, filename, path