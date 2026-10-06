import os
import sys
import json
from typing import Optional, Dict, Any

from ..core.enums import IssueType, Severity, Priority, MediaType, ReportStatus
from ..services.priority_service import normalize_priority


class NemotronService:
    """Service responsible for AI analysis using Nemotron model.

    Encapsulates the AI call so the rest of the application
    does not depend directly on provider-specific code.

    Environment configuration is read from environment variables.
    A deterministic demo fallback is provided when the real model
    is unavailable, so the hackathon demo workflow remains functional.
    """

    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "nemotron")
        self.model = os.getenv("AI_MODEL", "<configured-nemotron-model>")
        self.base_url = os.getenv("AI_BASE_URL", "")
        self.api_key = os.getenv("AI_API_KEY", "")

        # Demo mode: real API unavailable or credentials missing
        self.demo_mode = not self.api_key or self.api_key.startswith("<")

    # ------------------------------------------------------------------
    # Image analysis
    # ------------------------------------------------------------------

    def analyze_image(self, image_path: str, location: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze a single image frame.

        Returns structured analysis result matching our Pydantic schemas.
        """
        if self.demo_mode:
            return self._demo_analysis(
                issue_type=IssueType.POTHOLE,
                confidence=0.90,
                severity=Severity.HIGH,
                location=location,
            )

        # TODO: Real Nemotron API call when credentials/config are available
        # Example request structure:
        #   POST {base_url}/v1/chat/completions
        #   with image evidence and constrained instruction
        #   returning structured JSON matching our schema

        # Fallback to demo if real call fails
        return self._demo_analysis(
            issue_type=IssueType.POTHOLE,
            confidence=0.90,
            severity=Severity.HIGH,
            location=location,
        )

    # ------------------------------------------------------------------
    # Frame analysis (video)
    # ------------------------------------------------------------------

    def analyze_frame(self, frame_path: str, location: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze a single video frame image.

        Returns structured analysis result.
        """
        if self.demo_mode:
            return self._demo_analysis(
                issue_type=IssueType.POTHOLE,
                confidence=0.85,
                severity=Severity.MEDIUM,
                location=location,
            )

        # TODO: Real Nemotron frame analysis
        return self._demo_analysis(
            issue_type=IssueType.POTHOLE,
            confidence=0.85,
            severity=Severity.MEDIUM,
            location=location,
        )

    # ------------------------------------------------------------------
    # Demo fallback — deterministic, valid structured output
    # ------------------------------------------------------------------

    def _demo_analysis(
        self,
        issue_type: IssueType,
        confidence: float,
        severity: Severity,
        location: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Produce a valid structured analysis response from deterministic fallback.

        This method is the demo path. When Nemotron credentials/config
        are available, the real model call should replace this entirely.
        """
        from ..services.priority_service import normalize_priority

        return {
            "issue_detected": True,
            "issue_type": issue_type.value,
            "confidence": round(confidence, 2),
            "severity": severity.value,
            "priority": normalize_priority(severity.value),
            "description": self._build_description(issue_type),
            "recommended_action": self._build_recommended_action(issue_type, severity),
            "location": location or {},
        }

    @staticmethod
    def _build_description(issue_type: IssueType) -> str:
        """Build human-readable description from issue type."""
        descriptions = {
            IssueType.POTHOLE: "Large pothole detected on road surface.",
            IssueType.DAMAGED_ROAD: "Road surface damage detected.",
            IssueType.BROKEN_STREETLIGHT: "Broken streetlight observed.",
            IssueType.OVERFLOWING_DRAIN: "Overflowing drain detected.",
            IssueType.UNKNOWN: "Infrastructure issue detected.",
        }
        return descriptions.get(issue_type, "Infrastructure issue detected.")

    @staticmethod
    def _build_recommended_action(issue_type: IssueType, severity: Severity) -> str:
        """Build recommended action based on issue type and severity."""
        actions = {
            (IssueType.POTHOLE, Severity.CRITICAL): "Emergency road repair required.",
            (IssueType.POTHOLE, Severity.HIGH): "Schedule road repair urgently.",
            (IssueType.POTHOLE, Severity.MEDIUM): "Schedule road repair soon.",
            (IssueType.POTHOLE, Severity.LOW): "Monitor and plan maintenance.",
            (IssueType.DAMAGED_ROAD, Severity.CRITICAL): "Close road and schedule emergency repair.",
            (IssueType.DAMAGED_ROAD, Severity.HIGH): "Schedule road repair urgently.",
            (IssueType.DAMAGED_ROAD, Severity.MEDIUM): "Schedule road maintenance.",
            (IssueType.DAMAGED_ROAD, Severity.LOW): "Monitor and plan maintenance.",
            (IssueType.BROKEN_STREETLIGHT, Severity.CRITICAL): "Replace streetlight immediately.",
            (IssueType.BROKEN_STREETLIGHT, Severity.HIGH): "Schedule streetlight replacement urgently.",
            (IssueType.BROKEN_STREETLIGHT, Severity.MEDIUM): "Schedule streetlight maintenance.",
            (IssueType.BROKEN_STREETLIGHT, Severity.LOW): "Report and schedule replacement.",
            (IssueType.OVERFLOWING_DRAIN, Severity.CRITICAL): "Emergency drain clearing required.",
            (IssueType.OVERFLOWING_DRAIN, Severity.HIGH): "Clear drain urgently.",
            (IssueType.OVERFLOWING_DRAIN, Severity.MEDIUM): "Schedule drain clearing.",
            (IssueType.OVERFLOWING_DRAIN, Severity.LOW): "Monitor and plan maintenance.",
            (IssueType.UNKNOWN, Severity.CRITICAL): "Urgent investigation required.",
            (IssueType.UNKNOWN, Severity.HIGH): "Investigate and prioritize repair.",
            (IssueType.UNKNOWN, Severity.MEDIUM): "Schedule maintenance visit.",
            (IssueType.UNKNOWN, Severity.LOW): "Monitor and plan maintenance.",
        }
        key = (issue_type, severity)
        return actions.get(key, "Schedule maintenance and repair.")


# Convenience aliases so other modules can import NemotronService directly
nemotron_service = NemotronService()
analyze_image = nemotron_service.analyze_image
analyze_frame = nemotron_service.analyze_frame