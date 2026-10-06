BACKEND ARCHITECTURE
AI-Powered Public Infrastructure Monitoring
HACTOBERFEST '26

# 1. Architecture Objective

Build a reliable FastAPI backend that accepts image and video evidence, orchestrates Nemotron-based analysis, validates structured AI output, applies severity and priority rules, stores infrastructure reports, and exposes APIs to the frontend.

# 2. Backend Technology Stack

- Python
- FastAPI
- Pydantic
- OpenCV
- FFmpeg where required
- PostgreSQL
- SQLAlchemy
- Alembic
- Nemotron inference/orchestration layer

# 3. High-Level Backend Architecture

Frontend -> FastAPI API -> Validation -> Media Processing -> AI/Nemotron -> Output Validation -> Severity Engine -> Priority Engine -> Location/Report Service -> PostgreSQL

# 4. Suggested Folder Structure

backend/
  app/
    main.py
    config.py
    api/
      health.py
      analysis.py
      reports.py
    schemas/
      analysis.py
      report.py
      common.py
    services/
      image_service.py
      video_service.py
      ai_service.py
      severity_service.py
      priority_service.py
      location_service.py
      report_service.py
    models/
      report.py
    db/
      session.py
      base.py
    utils/
      media.py
      validation.py
      logging.py
  migrations/
  tests/

# 5. API Layer


# 6. Image Processing Architecture

Upload -> File Validation -> Temporary Storage -> Image Preprocessing -> Nemotron/AI Analysis -> Structured Output Validation -> Severity -> Priority -> Report
- Validate MIME type and file size.
- Generate safe temporary filename.
- Normalize/resize only when required by inference.
- Send visual evidence to the AI layer.
- Validate AI response with Pydantic.
- Apply business rules before persistence.

# 7. Video Processing Architecture

Video Upload -> Validation -> Metadata -> Frame Sampling -> Frame Extraction -> AI Analysis -> Timestamped Findings -> Temporal Aggregation -> Severity/Priority -> Report

## 7.1 Frame Sampling

Use a configurable sampling interval/FPS rather than analyzing every frame. Store the source timestamp for each analyzed frame.

## 7.2 Temporal Aggregation

Group repeated detections occurring close together in time. The MVP can use issue type + temporal proximity and simple evidence matching. Advanced tracking is a future enhancement.

# 8. Nemotron AI Service

The AI service is isolated behind a backend interface so the rest of the application does not depend directly on provider-specific code.
AI input: image/evidence frame plus a constrained instruction. AI output: structured JSON containing issue_detected, issue_type, confidence, severity, priority, description, and recommended_action.
The backend remains authoritative: AI output is validated and business rules may override or normalize severity/priority.

# 9. AI Output Schema

{
  "issue_detected": true,
  "issue_type": "pothole",
  "confidence": 0.94,
  "severity": "HIGH",
  "priority": "P2",
  "description": "Large pothole detected on road surface.",
  "recommended_action": "Schedule road repair urgently."
}

# 10. Severity Engine

Supported values: LOW, MEDIUM, HIGH, CRITICAL.
The engine should combine model output with deterministic validation/rules to keep results predictable and explainable.

# 11. Priority Engine

CRITICAL -> P1; HIGH -> P2; MEDIUM -> P3; LOW -> P4.
Priority should be derived server-side rather than accepted blindly from the frontend.

# 12. Location Service

- Accept browser/device coordinates from the client.
- Accept manual location when GPS is unavailable.
- Normalize latitude/longitude.
- Optionally resolve coordinates into a readable location name.
- Attach location to the report.

# 13. Database Architecture

PostgreSQL is the primary persistence layer. SQLAlchemy provides ORM access and Alembic manages migrations.
InfrastructureReport fields: id, media_type, media_url, issue_type, confidence, severity, priority, description, recommended_action, latitude, longitude, location_name, video_timestamp, status, created_at, updated_at.

# 14. Report Lifecycle

REPORTED -> AI_ANALYZED -> PRIORITIZED -> ASSIGNED -> IN_PROGRESS -> RESOLVED
Status transitions should be validated by the backend.

# 15. Storage Strategy

- Store media outside the database where practical; persist a media reference/URL in PostgreSQL.
- Use temporary storage during processing.
- Delete temporary files after successful processing when they are no longer required.
- Retain evidence-frame references for video reports.

# 16. Error Handling

Use a consistent API error envelope.
Example: {"success": false, "error": {"code": "INVALID_MEDIA", "message": "Unsupported video format."}}
- Invalid media -> 400
- Missing/invalid fields -> 422
- AI/provider failure -> controlled 502/503
- Missing report -> 404
- Unexpected server error -> 500 with safe message

# 17. Reliability and Fallbacks

- AI failure: controlled fallback/demo data path for hackathon presentation.
- GPS failure: manual location.
- Video processing failure: preserve usable extracted evidence where possible.
- Database failure: lightweight in-memory fallback may be used for the prototype.

# 18. Security

- Never expose Nemotron/provider credentials to the frontend.
- Validate MIME type and file size.
- Use safe temporary paths.
- Sanitize filenames.
- Limit upload size and processing duration.
- Validate all AI outputs.
- Do not trust client-provided severity or priority.

# 19. Performance

- Use frame sampling for video.
- Avoid loading entire large videos into memory where possible.
- Process long-running video jobs asynchronously if required.
- Cache repeated analysis only when safe and useful.
- Return analysis IDs for polling when processing is not immediate.

# 20. Backend Demo Flow

POST image/video -> validate -> process -> Nemotron -> validate output -> severity -> priority -> persist report -> return result -> frontend dashboard.

# 21. Backend Completion Criteria

- Image analysis endpoint works.
- Video analysis endpoint works.
- Nemotron integration is isolated and callable.
- AI schema validation works.
- Severity and priority are server-side.
- Reports persist correctly.
- Video timestamps are retained.
- Status updates are validated.
- Errors use a consistent response format.
- Frontend can consume every required endpoint.

# 22. Architecture Principle

Keep AI, media processing, business rules, persistence, and HTTP routes separated. This allows Nemotron to be changed or upgraded without rewriting the entire backend.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | /api/health | Service health |
| POST | /api/analyze/image | Image analysis |
| POST | /api/analyze/video | Video analysis |
| GET | /api/analysis/{id} | Analysis status/result |
| POST | /api/reports | Create report |
| GET | /api/reports | List reports |
| GET | /api/reports/{id} | Get report |
| PATCH | /api/reports/{id}/status | Update lifecycle status |
