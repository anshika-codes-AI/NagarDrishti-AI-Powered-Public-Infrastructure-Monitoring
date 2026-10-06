# API Integration Document

## AI-Powered Public Infrastructure Monitoring
### HACTOBERFEST '26

---

## 1. Purpose

This document defines the API integration contract between the Next.js frontend and FastAPI backend for the public infrastructure monitoring system.

The system supports:

- Image analysis
- Video analysis
- Infrastructure report creation
- Report retrieval
- Report status updates
- Health monitoring

The backend remains authoritative for AI results, severity, priority, validation, and report state.

---

## 2. Integration Architecture

```text
Next.js Frontend
       |
       | HTTP / JSON / Multipart
       v
FastAPI API Layer
       |
       +--> Validation
       |
       +--> Image Processing
       |
       +--> Video Processing
       |
       +--> Nemotron AI Service
       |
       +--> Severity Engine
       |
       +--> Priority Engine
       |
       +--> Report Service
       |
       v
PostgreSQL
```

---

## 3. Base URL

Development:

```text
http://localhost:8000
```

Frontend environment variable:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Production should use the deployed HTTPS backend URL.

---

## 4. Standard API Response

Successful response:

```json
{
  "success": true,
  "data": {}
}
```

Error response:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_MEDIA",
    "message": "Unsupported media format."
  }
}
```

The frontend must never depend on undocumented response fields.

---

# 5. Health API

## GET `/api/health`

Purpose:

- Check backend availability.
- Verify that the frontend can communicate with the backend.

Response:

```json
{
  "success": true,
  "data": {
    "status": "healthy"
  }
}
```

---

# 6. Image Analysis API

## POST `/api/analyze/image`

### Content Type

```text
multipart/form-data
```

### Request

```text
file: image file
latitude: optional
longitude: optional
location_name: optional
```

Example frontend request:

```typescript
const formData = new FormData();

formData.append("file", imageFile);

if (latitude) formData.append("latitude", String(latitude));
if (longitude) formData.append("longitude", String(longitude));
if (locationName) formData.append("location_name", locationName);

const response = await fetch(
  `${process.env.NEXT_PUBLIC_API_URL}/api/analyze/image`,
  {
    method: "POST",
    body: formData,
  }
);
```

### Successful Response

```json
{
  "success": true,
  "data": {
    "analysis_id": "analysis-001",
    "media_type": "image",
    "issue_detected": true,
    "issue_type": "pothole",
    "confidence": 0.94,
    "severity": "HIGH",
    "priority": "P2",
    "description": "Large pothole detected on road surface.",
    "recommended_action": "Schedule road repair urgently."
  }
}
```

---

# 7. Video Analysis API

## POST `/api/analyze/video`

### Content Type

```text
multipart/form-data
```

### Request

```text
file: video file
latitude: optional
longitude: optional
location_name: optional
```

### Processing

```text
Video
  |
  v
Validate
  |
  v
Read Metadata
  |
  v
Sample Frames
  |
  v
Nemotron Analysis
  |
  v
Timestamp Findings
  |
  v
Aggregate Repeated Issues
  |
  v
Severity + Priority
```

### Successful Response

For a short synchronous MVP:

```json
{
  "success": true,
  "data": {
    "analysis_id": "analysis-video-001",
    "media_type": "video",
    "duration_seconds": 28,
    "frames_analyzed": 14,
    "issues": [
      {
        "issue_type": "pothole",
        "confidence": 0.91,
        "severity": "HIGH",
        "priority": "P2",
        "timestamp_seconds": 8.4,
        "description": "Pothole detected.",
        "recommended_action": "Schedule road repair."
      }
    ]
  }
}
```

For longer videos, the API should return an `analysis_id` and allow the frontend to poll the analysis status.

---

# 8. Analysis Status API

## GET `/api/analysis/{analysis_id}`

Purpose:

Retrieve the current status/result of an image or video analysis.

Example:

```json
{
  "success": true,
  "data": {
    "analysis_id": "analysis-video-001",
    "status": "PROCESSING",
    "progress": 62
  }
}
```

Possible states:

```text
QUEUED
UPLOADING
PROCESSING
ANALYZING
GENERATING_REPORT
COMPLETED
FAILED
```

Completed response:

```json
{
  "success": true,
  "data": {
    "analysis_id": "analysis-video-001",
    "status": "COMPLETED",
    "progress": 100,
    "result": {}
  }
}
```

---

# 9. Create Report API

## POST `/api/reports`

Purpose:

Persist an analyzed infrastructure finding as an official report.

### Request

```json
{
  "analysis_id": "analysis-001",
  "media_type": "image",
  "media_url": "/media/example.jpg",
  "issue_type": "pothole",
  "confidence": 0.94,
  "severity": "HIGH",
  "priority": "P2",
  "description": "Large pothole detected on road surface.",
  "recommended_action": "Schedule road repair urgently.",
  "latitude": 22.7196,
  "longitude": 75.8577,
  "location_name": "Indore, Madhya Pradesh"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "report_id": "INF-0001",
    "status": "REPORTED"
  }
}
```

---

# 10. Get Reports API

## GET `/api/reports`

Purpose:

Return infrastructure reports for the dashboard.

Optional query parameters:

```text
issue_type
severity
priority
status
media_type
location
```

Example:

```text
GET /api/reports?severity=HIGH&status=OPEN
```

Response:

```json
{
  "success": true,
  "data": {
    "reports": [],
    "total": 0
  }
}
```

---

# 11. Get Single Report

## GET `/api/reports/{report_id}`

Response:

```json
{
  "success": true,
  "data": {
    "id": "INF-0001",
    "media_type": "image",
    "issue_type": "pothole",
    "confidence": 0.94,
    "severity": "HIGH",
    "priority": "P2",
    "description": "Large pothole detected.",
    "recommended_action": "Schedule road repair.",
    "status": "REPORTED",
    "latitude": 22.7196,
    "longitude": 75.8577,
    "location_name": "Indore, Madhya Pradesh"
  }
}
```

---

# 12. Update Report Status

## PATCH `/api/reports/{report_id}/status`

Request:

```json
{
  "status": "IN_PROGRESS"
}
```

Allowed lifecycle:

```text
REPORTED
   |
AI_ANALYZED
   |
PRIORITIZED
   |
ASSIGNED
   |
IN_PROGRESS
   |
RESOLVED
```

The backend must validate status transitions.

---

# 13. TypeScript API Types

```typescript
export type Severity =
  | "LOW"
  | "MEDIUM"
  | "HIGH"
  | "CRITICAL";

export type Priority =
  | "P1"
  | "P2"
  | "P3"
  | "P4";

export type ReportStatus =
  | "REPORTED"
  | "AI_ANALYZED"
  | "PRIORITIZED"
  | "ASSIGNED"
  | "IN_PROGRESS"
  | "RESOLVED";

export interface AnalysisResult {
  analysis_id: string;
  media_type: "image" | "video";
  issue_detected: boolean;
  issue_type: string;
  confidence: number;
  severity: Severity;
  priority: Priority;
  description: string;
  recommended_action: string;
}
```

---

# 14. Error Handling

Frontend must handle:

```text
400 INVALID_MEDIA
401 UNAUTHORIZED (if authentication is added)
404 NOT_FOUND
413 FILE_TOO_LARGE
422 VALIDATION_ERROR
502 AI_PROVIDER_ERROR
503 PROCESSING_UNAVAILABLE
500 INTERNAL_ERROR
```

UI behavior:

```text
API Error
   |
   v
Read error.code
   |
   v
Display user-friendly message
   |
   v
Offer Retry where appropriate
```

Never expose internal stack traces or provider secrets.

---

# 15. API Integration Rules

1. Centralize API calls in `lib/api.ts`.
2. Use typed request/response models.
3. Do not duplicate API URLs across components.
4. Do not trust client-provided severity or priority.
5. Show loading/progress state for long operations.
6. Handle failed uploads gracefully.
7. Use analysis IDs for long-running video jobs.
8. Keep the frontend independent from Nemotron-specific implementation details.

---

# 16. Recommended Frontend API Functions

```typescript
analyzeImage(file, location)
analyzeVideo(file, location)
getAnalysis(analysisId)
createReport(payload)
getReports(filters)
getReport(reportId)
updateReportStatus(reportId, status)
checkHealth()
```

---

# 17. End-to-End Integration Flow

## Image

```text
Upload Image
    ↓
POST /api/analyze/image
    ↓
Nemotron
    ↓
Structured Result
    ↓
POST /api/reports
    ↓
Dashboard
```

## Video

```text
Upload Video
    ↓
POST /api/analyze/video
    ↓
Frame Sampling
    ↓
Nemotron
    ↓
Timestamped Findings
    ↓
Aggregation
    ↓
POST /api/reports
    ↓
Dashboard
```

---

# 18. Integration Completion Criteria

- Health endpoint works.
- Image upload works.
- Video upload works.
- AI result schema is stable.
- Long video processing can expose status.
- Reports can be created and retrieved.
- Dashboard filters can query reports.
- Status updates work.
- Errors are consistently formatted.
