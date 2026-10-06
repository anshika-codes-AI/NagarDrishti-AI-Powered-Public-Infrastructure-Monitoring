from enum import Enum


class IssueType(str, Enum):
    POTHOLE = "pothole"
    DAMAGED_ROAD = "damaged_road"
    BROKEN_STREETLIGHT = "broken_streetlight"
    OVERFLOWING_DRAIN = "overflowing_drain"
    UNKNOWN = "unknown"


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Priority(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class ReportStatus(str, Enum):
    REPORTED = "REPORTED"
    AI_ANALYZED = "AI_ANALYZED"
    PRIORITIZED = "PRIORITIZED"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class MediaType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"


class AnalysisStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"