from pydantic import BaseModel, Field, validator
from typing import Optional
from ..core.enums import IssueType, Severity, Priority, ReportStatus, MediaType, AnalysisStatus


class HealthResponse(BaseModel):
    success: bool
    data: dict = {}


class AnalysisCreate(BaseModel):
    media_type: str
    issue_type: Optional[IssueType] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    severity: Optional[Severity] = None
    description: str = ""
    recommended_action: str = ""


class AnalysisStatusUpdate(BaseModel):
    status: AnalysisStatus


class AnalysisResponse(BaseModel):
    id: int
    media_type: str
    status: str
    issue_type: Optional[str] = None
    confidence: float
    severity: Optional[str] = None
    priority: str
    description: str
    recommended_action: str
    latitude: float = 0.0
    longitude: float = 0.0
    location_name: str = ""
    location_source: str = ""
    video_timestamp: str = ""
    error_message: Optional[str] = None
    created_at: str
    completed_at: Optional[str] = None

    class Config:
        from_attributes = True


class MediaCreate(BaseModel):
    media_type: MediaType
    filename: str
    file_path: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None


class MediaResponse(BaseModel):
    id: int
    analysis_id: Optional[int] = None
    media_type: str
    filename: str
    file_path: str
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
    created_at: str

    class Config:
        from_attributes = True


class ReportCreate(BaseModel):
    media_type: MediaType
    issue_type: IssueType
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    severity: Severity
    description: str = ""
    recommended_action: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    location_name: str = ""
    location_source: str = ""
    video_timestamp: str = ""

    @validator("issue_type", pre=True)
    def validate_issue_type(cls, v):
        if isinstance(v, str):
            return IssueType(v)
        return v


class ReportResponse(BaseModel):
    id: int
    media_type: str
    media_url: str = ""
    issue_type: str
    confidence: float
    severity: str
    priority: str
    description: str
    recommended_action: str
    latitude: float
    longitude: float
    location_name: str
    location_source: str
    video_timestamp: str
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ReportStatusUpdate(BaseModel):
    status: ReportStatus

    @validator("status", pre=True)
    def validate_status(cls, v):
        return ReportStatus(v)


class ErrorResponse(BaseModel):
    success: bool = False
    error: dict = {"code": "UNKNOWN", "message": "An unexpected error occurred"}