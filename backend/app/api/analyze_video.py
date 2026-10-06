import os
import uuid

import cv2

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    status,
)

from typing import Any, Dict, Optional

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
from ..core.config import settings
from ..services.nemotron_service import NemotronService


router = APIRouter(
    prefix="/api",
    tags=["analysis"],
)


def validate_uploaded_video(file: UploadFile) -> None:
    """Validate uploaded video file."""

    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_MEDIA",
                "message": "No file uploaded",
            },
        )

    allowed_types = [
        "video/mp4",
        "video/quicktime",
        "video/x-msvideo",
        "video/webm",
        "video/mpeg",
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_MEDIA",
                "message": (
                    f"Unsupported media type: "
                    f"{file.content_type}"
                ),
            },
        )

    max_size = 100 * 1024 * 1024

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


@router.post(
    "/analyze/video",
    response_model=Dict[str, Any],
)
async def analyze_video(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    location_name: Optional[str] = Form(None),
) -> Dict[str, Any]:

    temp_path: Optional[str] = None
    frame_samples = []

    # ---------------------------------------------------------
    # 1. Validate video
    # ---------------------------------------------------------
    validate_uploaded_video(file)

    # ---------------------------------------------------------
    # 2. Save uploaded video
    # ---------------------------------------------------------
    file_extension = os.path.splitext(
        file.filename or ""
    )[1].lower()

    if not file_extension:
        file_extension = ".mp4"

    safe_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

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

    # ---------------------------------------------------------
    # 4. Extract sampled frames
    # ---------------------------------------------------------
    try:
        cap = cv2.VideoCapture(temp_path)

        if not cap.isOpened():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "VIDEO_PROCESSING_FAILED",
                    "message": "Could not open video file",
                },
            )

        total_frames = int(
            cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        fps = cap.get(cv2.CAP_PROP_FPS)

        duration = (
            total_frames / fps
            if fps > 0
            else 0
        )

        sample_interval = 5

        if hasattr(
            settings,
            "VIDEO_FRAME_SAMPLE_INTERVAL",
        ):
            try:
                sample_interval = max(
                    1,
                    int(
                        settings.VIDEO_FRAME_SAMPLE_INTERVAL
                    ),
                )
            except Exception:
                sample_interval = 5

        frame_indices = list(
            range(
                0,
                total_frames,
                sample_interval,
            )
        )

        if not frame_indices and total_frames > 0:
            frame_indices = [0]

        for idx in frame_indices:
            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                idx,
            )

            ret, frame = cap.read()

            if not ret:
                continue

            frame_filename = (
                f"frame_{idx}_{uuid.uuid4()}.jpg"
            )

            frame_path = os.path.join(
                "media",
                "uploads",
                frame_filename,
            )

            success = cv2.imwrite(
                frame_path,
                frame,
            )

            if success:
                frame_samples.append(
                    frame_path
                )

        cap.release()

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "VIDEO_PROCESSING_FAILED",
                "message": str(e),
            },
        )

    # ---------------------------------------------------------
    # 5. Dispatch video analysis
    # ---------------------------------------------------------
    try:
        dispatch_result = Dispatcher.dispatch(
            "video",
            temp_path,
            location,
        )

        if not dispatch_result:
            raise RuntimeError(
                "Video dispatcher returned no result."
            )

        analysis_result = dispatch_result.get(
            "analysis",
            {},
        )

        # -----------------------------------------------------
        # 6. Demo fallback if no usable result
        # -----------------------------------------------------
        if not analysis_result:
            nemotron = NemotronService()

            if frame_samples:
                analysis_result = (
                    nemotron.analyze_frame(
                        frame_path=frame_samples[0],
                        location=location,
                    )
                )
            else:
                analysis_result = (
                    nemotron.analyze_frame(
                        frame_path="",
                        location=location,
                    )
                )

        if not analysis_result:
            raise RuntimeError(
                "AI analysis returned no result."
            )

        # -----------------------------------------------------
        # 7. Normalize AI result
        # -----------------------------------------------------
        media_type_value = analysis_result.get(
            "media_type",
            MediaType.VIDEO.value,
        )

        issue_type_value = analysis_result.get(
            "issue_type",
            IssueType.POTHOLE.value,
        )

        confidence_value = float(
            analysis_result.get(
                "confidence",
                0.85,
            )
        )

        severity_value = analysis_result.get(
            "severity",
            Severity.MEDIUM.value,
        )

        priority_value = analysis_result.get(
            "priority",
            Priority.P3.value,
        )

        description_value = analysis_result.get(
            "description",
            "Infrastructure issue detected in video.",
        )

        recommended_action_value = (
            analysis_result.get(
                "recommended_action",
                "Inspect and repair the reported infrastructure.",
            )
        )

        latitude_value = analysis_result.get(
            "latitude",
            latitude,
        )

        longitude_value = analysis_result.get(
            "longitude",
            longitude,
        )

        location_name_value = analysis_result.get(
            "location_name",
            location_name or "",
        )

        issue_detected_value = bool(
            analysis_result.get(
                "issue_detected",
                True,
            )
        )

        # -----------------------------------------------------
        # 8. Database
        # -----------------------------------------------------
        db = SessionLocal()

        try:
            # ---------------------------------------------
            # Analysis
            # ---------------------------------------------
            analysis = Analysis(
                media_type=media_type_value,
                status="COMPLETED",
                issue_type=IssueType(
                    issue_type_value
                ),
                confidence=confidence_value,
                severity=Severity(
                    severity_value
                ),
                priority=Priority(
                    priority_value
                ),
                description=description_value,
                recommended_action=(
                    recommended_action_value
                ),
                latitude=latitude_value,
                longitude=longitude_value,
                location_name=location_name_value,
                location_source="uploaded_video",
                video_timestamp="",
                error_message=None,
            )

            db.add(analysis)
            db.flush()

            # ---------------------------------------------
            # Media
            # ---------------------------------------------
            media = Media(
                analysis_id=analysis.id,
                media_type=media_type_value,
                filename=(
                    file.filename
                    or safe_filename
                ),
                file_path=temp_path,
                mime_type=file.content_type,
                file_size=len(content),
            )

            db.add(media)

            # ---------------------------------------------
            # Report
            # ---------------------------------------------
            report = InfrastructureReport(
                analysis_id=analysis.id,
                media_type=media_type_value,
                media_url=temp_path,
                issue_type=IssueType(
                    issue_type_value
                ),
                confidence=confidence_value,
                severity=Severity(
                    severity_value
                ),
                priority=Priority(
                    priority_value
                ),
                description=description_value,
                recommended_action=(
                    recommended_action_value
                ),
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
                status=(
                    ReportStatus.REPORTED.value
                ),
            )

            db.add(report)

            # ---------------------------------------------
            # Commit
            # ---------------------------------------------
            db.commit()

            db.refresh(analysis)
            db.refresh(media)
            db.refresh(report)

            # ---------------------------------------------
            # Response
            # ---------------------------------------------
            response_data = {
                "analysis_id": analysis.id,
                "report_id": report.id,
                "media_type": media_type_value,
                "issue_detected": (
                    issue_detected_value
                ),
                "issue_type": issue_type_value,
                "confidence": confidence_value,
                "severity": severity_value,
                "priority": priority_value,
                "description": description_value,
                "recommended_action": (
                    recommended_action_value
                ),
                "video_duration": duration,
                "frames_sampled": len(
                    frame_samples
                ),
            }

            return {
                "success": True,
                "data": response_data,
            }

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "ANALYSIS_FAILED",
                "message": str(e),
            },
        )

    finally:
        # -----------------------------------------------------
        # Cleanup sampled frames
        # -----------------------------------------------------
        for frame_path in frame_samples:
            try:
                if os.path.exists(frame_path):
                    os.remove(frame_path)
            except Exception:
                pass

        # -----------------------------------------------------
        # Cleanup uploaded video
        # -----------------------------------------------------
        if temp_path:
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except Exception:
                pass