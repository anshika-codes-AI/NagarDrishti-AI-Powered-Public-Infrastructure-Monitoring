from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..core.enums import IssueType, Severity, Priority, ReportStatus, MediaType
from ..services.priority_service import normalize_priority

from ..models.report import InfrastructureReport
from ..models.analysis import Analysis
from ..schemas.common import (
    ReportCreate,
    ReportResponse,
    ReportStatusUpdate,
    AnalysisCreate,
    AnalysisResponse,
    MediaCreate,
    MediaResponse,
)
from ..db.base import Base
from typing import Optional

router = APIRouter(prefix="/api", tags=["reports"])


# Dependency to get analysis by ID, or raise 404
def get_analysis_or_404(db: Session, analysis_id: int) -> Analysis:
    analysis = db.get(Analysis, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "ANALYSIS_NOT_FOUND", "message": "Analysis not found"},
        )
    return analysis


@router.post("/reports", response_model=ReportResponse)
async def create_report(
    *,
    db: Session = Depends(get_db),
    report_in: ReportCreate,
) -> ReportResponse:
    """Create a new infrastructure report.

    Priority is automatically derived from severity using backend rules.
    Client-provided priority is ignored; backend mapping is authoritative.
    """
    # Calculate priority from severity (backend authoritative)
    calculated_priority = normalize_priority(report_in.severity)

    db_report = InfrastructureReport(
        media_type=report_in.media_type,
        media_url="",
        issue_type=report_in.issue_type.value if isinstance(report_in.issue_type, IssueType) else report_in.issue_type,
        confidence=report_in.confidence,
        severity=report_in.severity.value if isinstance(report_in.severity, Severity) else report_in.severity,
        priority=calculated_priority,
        description=report_in.description,
        recommended_action=report_in.recommended_action,
        latitude=report_in.latitude,
        longitude=report_in.longitude,
        location_name=report_in.location_name,
        location_source=report_in.location_source,
        video_timestamp=report_in.video_timestamp,
        status="REPORTED",
    )

    db.add(db_report)
    db.commit()
    db.refresh(db_report)

    return ReportResponse.model_validate(db_report)


@router.get("/reports", response_model=list[ReportResponse])
async def list_reports(
    *,
    db: Session = Depends(get_db),
    issue_type: Optional[IssueType] = None,
    severity: Optional[Severity] = None,
    priority: Optional[Priority] = None,
    status: Optional[ReportStatus] = None,
    media_type: Optional[MediaType] = None,
) -> list[ReportResponse]:
    """List infrastructure reports with optional filters."""
    query = db.query(InfrastructureReport)

    if issue_type is not None:
        query = query.filter(InfrastructureReport.issue_type == issue_type.value)
    if severity is not None:
        query = query.filter(InfrastructureReport.severity == severity.value)
    if priority is not None:
        query = query.filter(InfrastructureReport.priority == priority.value)
    if status is not None:
        query = query.filter(InfrastructureReport.status == status.value)
    if media_type is not None:
        query = query.filter(InfrastructureReport.media_type == media_type.value)

    reports = query.order_by(InfrastructureReport.created_at.desc()).all()

    return [ReportResponse.model_validate(r) for r in reports]


@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(
    *,
    db: Session = Depends(get_db),
    report_id: int,
) -> ReportResponse:
    """Get a single infrastructure report."""
    report = db.get(InfrastructureReport, report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "REPORT_NOT_FOUND", "message": "Report not found"},
        )

    return ReportResponse.model_validate(report)


@router.patch("/reports/{report_id}/status", response_model=ReportResponse)
async def update_report_status(
    *,
    db: Session = Depends(get_db),
    report_id: int,
    status_in: ReportStatusUpdate,
) -> ReportResponse:
    """Update report status.

    Validates the new status against allowed ReportStatus values.
    """
    report = db.get(InfrastructureReport, report_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "REPORT_NOT_FOUND", "message": "Report not found"},
        )

    report.status = status_in.status.value if isinstance(status_in.status, ReportStatus) else status_in.status
    db.add(report)
    db.commit()
    db.refresh(report)

    return ReportResponse.model_validate(report)