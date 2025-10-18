from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.sql import func
from ..utils.db import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    status = Column(String)  # Enum-like: "queued", "processing", "completed", or "failed"
    request_payload = Column(JSON)
    result_payload = Column(JSON, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())