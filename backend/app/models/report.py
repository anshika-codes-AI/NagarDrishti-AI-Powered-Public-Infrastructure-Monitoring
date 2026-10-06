from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from ..db.base import Base


class InfrastructureReport(Base):
    __tablename__ = "infrastructure_reports"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)

    analysis_id = Column(Integer, nullable=True, index=True)

    media_type = Column(String, nullable=False)
    media_url = Column(String, nullable=True)

    issue_type = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)

    severity = Column(String, nullable=False)
    priority = Column(String, nullable=False)

    description = Column(Text, nullable=True)
    recommended_action = Column(Text, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_name = Column(String, nullable=True)

    video_timestamp = Column(String, nullable=True)

    status = Column(
        String,
        nullable=False,
        default="REPORTED",
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )