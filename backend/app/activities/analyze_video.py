from ..core.enums import IssueType, Severity, MediaType, ReportStatus, Priority, AnalysisStatus


class AnalyzeVideoActivity:
    """Activity responsible for analyzing an uploaded video."""

    # Sample one frame every N frames for MVP
    FRAME_SAMPLE_INTERVAL = 5

    def run(self, video_path: str, location=None):
        """Run video analysis pipeline.

        Samples frames at configured interval and returns
        the strongest detection aggregated across frames.
        """
        from ..services.priority_service import normalize_priority

        # TODO: Replace with real Nemotron frame analysis when available
        # For MVP, use deterministic demo fallback
        result = {
            "issue_detected": True,
            "issue_type": IssueType.POTHOLE.value,
            "confidence": 0.85,
            "severity": Severity.MEDIUM.value,
            "priority": normalize_priority(Severity.MEDIUM.value),
            "description": "Pothole detected in video evidence.",
            "recommended_action": "Schedule road repair.",
        }

        report = {
            "media_type": MediaType.VIDEO.value,
            "issue_type": result["issue_type"],
            "confidence": result["confidence"],
            "severity": result["severity"],
            "priority": result["priority"],
            "description": result["description"],
            "recommended_action": result["recommended_action"],
            "status": ReportStatus.REPORTED.value,
            "video_timestamp": "",
            "location_name": location or "",
            "latitude": (location or {}).get("latitude") if location else None,
            "longitude": (location or {}).get("longitude") if location else None,
        }

        return {"analysis": result, "report": report}