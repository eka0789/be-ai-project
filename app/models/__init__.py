from ..utils.db import Base, engine
from .document_model import Document
from .job_model import Job


def init_db() -> None:
    """Initialize the database by creating all tables defined in the models."""
    Base.metadata.create_all(bind=engine)