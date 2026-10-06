from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..db.base import Base


class Media(Base):
    __tablename__ = "media"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, nullable=True)
    media_type = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    mime_type = Column(String, nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship back to analysis
    analysis = None  # placeholder for relationship