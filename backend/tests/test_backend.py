"""Backend tests for TASK 02: Data layer + core API foundation.

These tests import modules individually to avoid circular import issues
with the FastAPI API routers.
"""

import sys
import os

# Add directories to path individually to avoid triggering
# backend/app/__init__.py circular imports

# 1. Add the backend directory itself
backend_dir = r"A:\AI-Powered Public Infra Monitoring\backend"
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 2. Add the core directory
core_dir = os.path.join(backend_dir, "app", "core")
if core_dir not in sys.path:
    sys.path.insert(0, core_dir)

# 3. Add the services directory
services_dir = os.path.join(backend_dir, "app", "services")
if services_dir not in sys.path:
    sys.path.insert(0, services_dir)

# 4. Add the schemas directory
schemas_dir = os.path.join(backend_dir, "app", "schemas")
if schemas_dir not in sys.path:
    sys.path.insert(0, schemas_dir)

# 5. Add the models directory
models_dir = os.path.join(backend_dir, "app", "models")
if models_dir not in sys.path:
    sys.path.insert(0, models_dir)

# Now import the specific modules we need

# Enums - can be imported directly from core
from core.enums import (
    IssueType,
    Severity,
    Priority,
    ReportStatus,
    MediaType,
    AnalysisStatus,
)

# Priority service
from services.priority_service import normalize_priority

# Schemas
from schemas.common import (
    AnalysisCreate,
    ReportCreate,
    ReportStatusUpdate,
    ErrorResponse,
)


class TestSeverityPriorityMapping:
    """Test the severity → priority mapping is deterministic and correct."""

    def test_critical_to_p1(self) -> None:
        assert normalize_priority("CRITICAL") == "P1"

    def test_high_to_p2(self) -> None:
        assert normalize_priority("HIGH") == "P2"

    def test_medium_to_p3(self) -> None:
        assert normalize_priority("MEDIUM") == "P3"

    def test_low_to_p4(self) -> None:
        assert normalize_priority("LOW") == "P4"

    def test_unknown_severity_raises(self) -> None:
        try:
            normalize_priority("UNKNOWN")
            assert False, "Should have raised an exception"
        except (ValueError, TypeError):
            pass


class TestEnums:
    """Test that all enum values are correct and consistent."""

    def test_issue_type_enum(self) -> None:
        assert IssueType.POTHOLE.value == "pothole"
        assert IssueType.DAMAGED_ROAD.value == "damaged_road"
        assert IssueType.BROKEN_STREETLIGHT.value == "broken_streetlight"
        assert IssueType.OVERFLOWING_DRAIN.value == "overflowing_drain"
        assert IssueType.UNKNOWN.value == "unknown"

    def test_severity_enum(self) -> None:
        assert Severity.LOW.value == "LOW"
        assert Severity.MEDIUM.value == "MEDIUM"
        assert Severity.HIGH.value == "HIGH"
        assert Severity.CRITICAL.value == "CRITICAL"

    def test_priority_enum(self) -> None:
        assert Priority.P1.value == "P1"
        assert Priority.P2.value == "P2"
        assert Priority.P3.value == "P3"
        assert Priority.P4.value == "P4"

    def test_report_status_enum(self) -> None:
        assert ReportStatus.REPORTED.value == "REPORTED"
        assert ReportStatus.AI_ANALYZED.value == "AI_ANALYZED"
        assert ReportStatus.PRIORITIZED.value == "PRIORITIZED"
        assert ReportStatus.ASSIGNED.value == "ASSIGNED"
        assert ReportStatus.IN_PROGRESS.value == "IN_PROGRESS"
        assert ReportStatus.RESOLVED.value == "RESOLVED"

    def test_media_type_enum(self) -> None:
        assert MediaType.IMAGE.value == "IMAGE"
        assert MediaType.VIDEO.value == "VIDEO"

    def test_analysis_status_enum(self) -> None:
        assert AnalysisStatus.PENDING.value == "PENDING"
        assert AnalysisStatus.PROCESSING.value == "PROCESSING"
        assert AnalysisStatus.COMPLETED.value == "COMPLETED"
        assert AnalysisStatus.FAILED.value == "FAILED"


class TestSchemaValidation:
    """Test Pydantic schema validation."""

    def test_analysis_create_valid(self) -> None:
        """Create a valid AnalysisCreate schema."""
        data = {
            "media_type": "IMAGE",
            "issue_type": "pothole",
            "confidence": 0.94,
            "severity": "HIGH",
            "description": "Large pothole detected",
        }
        schema = AnalysisCreate(**data)
        assert schema.media_type == "IMAGE"
        assert schema.confidence == 0.94
        assert schema.severity == "HIGH"

    def test_analysis_create_with_defaults(self) -> None:
        """Create AnalysisCreate with default values."""
        schema = AnalysisCreate(media_type="IMAGE")
        assert schema.media_type == "IMAGE"
        assert schema.issue_type is None
        assert schema.confidence == 0.0
        assert schema.severity is None

    def test_report_create_valid(self) -> None:
        """Create a valid ReportCreate schema with priority auto-set."""
        data = {
            "media_type": "VIDEO",
            "issue_type": "broken_streetlight",
            "confidence": 0.88,
            "severity": "CRITICAL",
            "description": "Broken streetlight",
            "recommended_action": "Urgent repair",
        }
        schema = ReportCreate(**data)
        assert schema.media_type == "VIDEO"
        assert schema.severity == "CRITICAL"
        # Priority should be automatically set from severity (CRITICAL → P1)
        assert schema.priority == "P1"

    def test_report_status_update_valid(self) -> None:
        """Create a ReportStatusUpdate schema with valid values."""
        for status_name in ["REPORTED", "AI_ANALYZED", "PRIORITIZED", "ASSIGNED", "IN_PROGRESS", "RESOLVED"]:
            schema = ReportStatusUpdate(status=status_name)
            # Should not raise ValidationError

    def test_report_status_update_invalid(self) -> None:
        """Create a ReportStatusUpdate schema with invalid status should fail."""
        try:
            schema = ReportStatusUpdate(status="INVALID")
            assert False, "Should have raised ValidationError"
        except ValidationError:
            pass

    def test_error_response_defaults(self) -> None:
        """ErrorResponse should have sensible defaults."""
        err = ErrorResponse()
        assert err.success is False
        assert "code" in err.error
        assert "message" in err.error


class TestPriorityFromSeverityRule:
    """Test that the backend severity→priority rule is authoritative."""

    def test_p1_is_only_for_critical(self) -> None:
        """Only CRITICAL severity should produce P1 priority."""
        for severity, expected in [
            ("LOW", "P4"),
            ("MEDIUM", "P3"),
            ("HIGH", "P2"),
            ("CRITICAL", "P1"),
        ]:
            result = normalize_priority(severity)
            assert result == expected, f"{severity} → {result}, expected {expected}"

    def test_p4_is_only_for_low(self) -> None:
        """Only LOW severity should produce P4 priority."""
        result = normalize_priority("LOW")
        assert result == "P4"

    def test_all_severities_map_to_priorities(self) -> None:
        """All severity values should map to valid priority values."""
        for severity in Severity:
            priority = normalize_priority(severity.value)
            assert priority in [p.value for p in Priority]


class TestIssueTypeValidation:
    """Test IssueType validation in schemas."""

    def test_issue_type_in_report_create(self) -> None:
        """IssueType should be validated in ReportCreate."""
        data = {
            "media_type": "IMAGE",
            "issue_type": "pothole",
            "confidence": 0.9,
            "severity": "HIGH",
            "description": "Test",
            "recommended_action": "Test",
        }
        schema = ReportCreate(**data)
        assert schema.issue_type.value == "pothole"


class TestConfidenceRange:
    """Test confidence value range validation."""

    def test_confidence_valid_range(self) -> None:
        """Confidence should accept values 0.0 to 1.0."""
        a = AnalysisCreate(media_type="IMAGE", confidence=0.0)
        b = AnalysisCreate(media_type="IMAGE", confidence=1.0)
        c = AnalysisCreate(media_type="IMAGE", confidence=0.5)
        assert a.confidence == 0.0
        assert b.confidence == 1.0
        assert c.confidence == 0.5

    def test_confidence_out_of_range(self) -> None:
        """Confidence outside 0.0-1.0 should be rejected by Pydantic."""
        try:
            AnalysisCreate(media_type="IMAGE", confidence=1.5)
            assert False, "Should have raised ValidationError for confidence > 1.0"
        except Exception:
            pass

        try:
            AnalysisCreate(media_type="IMAGE", confidence=-0.1)
            assert False, "Should have raised ValidationError for confidence < 0.0"
        except Exception:
            pass


class TestDirectImport:
    """Test that we can import key modules without circular dependency issues."""

    def test_import_enums(self) -> None:
        from backend.app.core.enums import IssueType  # noqa: F401
        assert IssueType.POTHOLE.value == "pothole"

    def test_import_schemas(self) -> None:
        from backend.app.schemas.common import AnalysisCreate  # noqa: F401
        schema = AnalysisCreate(media_type="IMAGE")
        assert schema.media_type == "IMAGE"

    def test_import_services(self) -> None:
        from backend.app.services.priority_service import normalize_priority  # noqa: F401
        result = normalize_priority("HIGH")
        assert result == "P2"