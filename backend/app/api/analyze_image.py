from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Any, Dict, Optional
import os
import uuid

from ..core.enums import (
    IssueType,
    Severity,
    MediaType,
    ReportStatus,
    Priority,
)
from ..dispatcher import Dispatcher
from ..schemas.common import ReportCreate
from ..models.analysis import Analysis
from ..models.media import Media
from ..models.report import InfrastructureReport
from ..db.session import SessionLocal


router = APIRouter(prefix="/api", tags=["analysis"])


def validate_uploaded_image(file: UploadFile) -> None:
    """Validate uploaded image file."""

    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_MEDIA",
                "message": "No file uploaded",
            },
        )

    allowed_types = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/webp",
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_MEDIA",
                "message": f"Unsupported media type: {file.content_type}",
            },
        )

    max_size = 10 * 1024 * 1024

    content = file.file.read()

    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "MEDIA_TOO_LARGE",
                "message": (
                    f"File too large: {len(content)} bytes "
                    f"(max {max_size})"
                ),
            },
        )

    file.file.seek(0)


@router.post("/analyze/image", response_model=Dict[str, Any])
async def analyze_image(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    location_name: Optional[str] = Form(None),
) -> Dict[str, Any]:

    # ---------------------------------------------------------
    # 1. Validate uploaded image
    # ---------------------------------------------------------
    validate_uploaded_image(file)

    # ---------------------------------------------------------
    # 2. Save temporary media
    # ---------------------------------------------------------
    file_extension = os.path.splitext(
        file.filename or ""
    )[1].lower()

    if not file_extension:
        file_extension = ".jpg"

    safe_filename = f"{uuid.uuid4()}{file_extension}"

    temp_path = os.path.join(
        "media",
        "uploads",
        safe_filename,
    )

    os.makedirs(
        os.path.dirname(temp_path),
        exist_ok=True,
    )

    content = file.file.read()

    with open(temp_path, "wb") as output_file:
        output_file.write(content)

    # ---------------------------------------------------------
    # 3. Prepare location
    # ---------------------------------------------------------
    location: Dict[str, Any] = {}

    if latitude is not None:
        location["latitude"] = latitude

    if longitude is not None:
        location["longitude"] = longitude

    if location_name:
        location["location_name"] = location_name

    db = SessionLocal()

    try:
        # -----------------------------------------------------
        # 4. Run AI analysis
        # -----------------------------------------------------
        dispatch_result = Dispatcher.dispatch(
            "image",
            temp_path,
            location,
        )

        if not dispatch_result:
            raise RuntimeError(
                "AI dispatcher returned no result."
            )

        analysis_result = dispatch_result.get(
            "analysis",
            {},
        )

        report_data = dispatch_result.get(
            "report",
            {},
        )

        if not report_data:
            raise RuntimeError(
                "AI analysis did not return report data."
            )

        # -----------------------------------------------------
        # 5. Safely extract values
        # -----------------------------------------------------
        media_type_value = report_data.get(
            "media_type",
            "image",
        )

        issue_type_value = report_data.get(
            "issue_type",
            "Unknown",
        )

        confidence_value = float(
            report_data.get("confidence", 0.0)
        )

        severity_value = report_data.get(
            "severity",
            "LOW",
        )

        priority_value = report_data.get(
            "priority",
            "P4",
        )

        description_value = report_data.get(
            "description",
            "Infrastructure issue detected.",
        )

        recommended_action_value = report_data.get(
            "recommended_action",
            "Inspect and repair the reported infrastructure.",
        )

        latitude_value = report_data.get(
            "latitude",
            latitude,
        )

        longitude_value = report_data.get(
            "longitude",
            longitude,
        )

        location_name_value = report_data.get(
            "location_name",
            location_name or "",
        )

        # -----------------------------------------------------
        # 6. Create Analysis record
        # -----------------------------------------------------
        analysis = Analysis(
            media_type=media_type_value,
            status="COMPLETED",
            issue_type=IssueType(issue_type_value),
            confidence=confidence_value,
            severity=Severity(severity_value),
            priority=Priority(priority_value),
            description=description_value,
            recommended_action=recommended_action_value,
            latitude=latitude_value,
            longitude=longitude_value,
            location_name=location_name_value,
            location_source="uploaded_image",
            video_timestamp="",
            error_message=None,
        )

        db.add(analysis)
        db.flush()

        # -----------------------------------------------------
        # 7. Create Media record
        # -----------------------------------------------------
        media = Media(
            analysis_id=analysis.id,
            media_type=media_type_value,
            filename=file.filename or safe_filename,
            file_path=temp_path,
            mime_type=file.content_type,
            file_size=len(content),
        )

        db.add(media)

        # -----------------------------------------------------
        # 8. Create Infrastructure Report
        # -----------------------------------------------------
        report = InfrastructureReport(
            analysis_id=analysis.id,
            media_type=media_type_value,
            media_url=temp_path,
            issue_type=IssueType(issue_type_value),
            confidence=confidence_value,
            severity=Severity(severity_value),
            priority=Priority(priority_value),
            description=description_value,
            recommended_action=recommended_action_value,
            latitude=(
                latitude_value
                if latitude_value is not None
                else 0.0
            ),
            longitude=(
                longitude_value
                if longitude_value is not None
                else 0.0
            ),
            location_name=location_name_value,
            video_timestamp="",
            status=ReportStatus.REPORTED.value,
        )

        db.add(report)

        # -----------------------------------------------------
        # 9. Commit everything
        # -----------------------------------------------------
        db.commit()

        db.refresh(analysis)
        db.refresh(media)
        db.refresh(report)

        # -----------------------------------------------------
        # 10. Build API response
        # -----------------------------------------------------
        response_data = {
            "analysis_id": analysis.id,
            "report_id": report.id,
            "media_type": media_type_value,
            "issue_detected": bool(
                analysis_result.get(
                    "issue_detected",
                    True,
                )
            ),
            "issue_type": analysis_result.get(
                "issue_type",
                issue_type_value,
            ),
            "confidence": float(
                analysis_result.get(
                    "confidence",
                    confidence_value,
                )
            ),
            "severity": analysis_result.get(
                "severity",
                severity_value,
            ),
            "priority": analysis_result.get(
                "priority",
                priority_value,
            ),
            "description": analysis_result.get(
                "description",
                description_value,
            ),
            "recommended_action": analysis_result.get(
                "recommended_action",
                recommended_action_value,
            ),
        }

        return {
            "success": True,
            "data": response_data,
        }

    except HTTPException:
        db.rollback()

        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

        raise

    except Exception as e:
        db.rollback()

        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "ANALYSIS_FAILED",
                "message": str(e),
            },
        )

    finally:
        db.close()