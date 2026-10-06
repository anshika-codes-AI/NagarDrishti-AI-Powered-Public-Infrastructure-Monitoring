from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from ..db.base import Base


class Analysis(Base):
    __tablename__ = "analyses"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    media_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="PENDING")

    issue_type = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)

    severity = Column(String, nullable=True)
    priority = Column(String, nullable=True)

    description = Column(String, nullable=True)
    recommended_action = Column(String, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    location_name = Column(String, nullable=True)
    location_source = Column(String, nullable=True)

    video_timestamp = Column(String, nullable=True)

    error_message = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    completed_at = Column(DateTime, nullable=True)