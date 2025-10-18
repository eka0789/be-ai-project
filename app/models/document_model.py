from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from ..utils.db import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String, unique=True, index=True)
    filename = Column(String)
    path = Column(String)
    kind = Column(String)  # Enum-like: "cv", "report", or "internal"
    created_at = Column(DateTime(timezone=True), server_default=func.now())