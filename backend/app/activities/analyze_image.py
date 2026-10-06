from ..core.enums import IssueType, Severity, MediaType, ReportStatus, Priority


class AnalyzeImageActivity:
    """Activity responsible for analyzing an uploaded image."""

    def run(self, image_path: str, location=None):
        """Run image analysis pipeline.

        Returns dict with analysis results.
        """
        from ..services.priority_service import normalize_priority

        # TODO: Replace with real Nemotron call when available
        # For now use demo fallback
        result = {
            "issue_detected": True,
            "issue_type": IssueType.POTHOLE.value,
            "confidence": 0.90,
            "severity": Severity.HIGH.value,
            "priority": normalize_priority(Severity.HIGH.value),
            "description": "Large pothole detected on road surface.",
            "recommended_action": "Schedule road repair urgently.",
        }

        report = {
            "media_type": MediaType.IMAGE.value,
            "issue_type": result["issue_type"],
            "confidence": result["confidence"],
            "severity": result["severity"],
            "priority": result["priority"],
            "description": result["description"],
            "recommended_action": result["recommended_action"],
            "status": ReportStatus.REPORTED.value,
            "location_name": location or "",
            "latitude": (location or {}).get("latitude") if location else None,
            "longitude": (location or {}).get("longitude") if location else None,
        }

        return {"analysis": result, "report": report}