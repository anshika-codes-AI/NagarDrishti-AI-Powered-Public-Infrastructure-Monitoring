# AGENTS.md

# HACTOBERFEST '26 — AI-Powered Public Infrastructure Monitoring

## 1. Mission

Build a working hackathon MVP that accepts **both images and videos** of public infrastructure, analyzes the visual evidence with the configured **Nemotron AI layer**, detects and classifies infrastructure issues, determines severity and priority, attaches location information when available, creates actionable reports, and displays them through a monitoring dashboard.

The core product flow is:

```text
IMAGE / VIDEO
     ↓
MEDIA VALIDATION
     ↓
AI / NEMOTRON ANALYSIS
     ↓
ISSUE DETECTION
     ↓
CLASSIFICATION
     ↓
SEVERITY
     ↓
PRIORITY
     ↓
LOCATION
     ↓
INFRASTRUCTURE REPORT
     ↓
DASHBOARD
     ↓
ACTION / STATUS
```

---

# 2. Source Problem Scope

The official HACTOBERFEST '26 problem statement requires an AI-based system for public infrastructure issues such as:

- Potholes
- Damaged roads
- Broken streetlights
- Overflowing drains

The system must:

1. Detect issues.
2. Classify issues.
3. Prioritize issues.
4. Support faster action.

Image and video analysis are implementation choices that extend this core problem into a practical inspection workflow.

Do not change the core problem into a generic computer-vision demo or a generic chatbot.

---

# 3. Non-Negotiable Product Requirements

The MVP MUST support:

### Image

```text
Upload/Capture
→ Analyze
→ Detect
→ Classify
→ Confidence
→ Severity
→ Priority
→ Report
```

### Video

```text
Upload
→ Validate
→ Extract/Sample Frames
→ Analyze Frames
→ Timestamp Findings
→ Aggregate Repeated Findings
→ Severity
→ Priority
→ Report
```

### Dashboard

```text
Reports
→ Filter
→ Inspect
→ View Location
→ View Evidence
→ Update Status
```

---

# 4. Technology Stack

## Frontend

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query / React Query
- Leaflet or equivalent map library

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL

## Media Processing

- OpenCV
- FFmpeg where required

## AI

- Nemotron as the primary configured AI/reasoning layer

Do not introduce another major AI provider or framework unless the existing Nemotron setup cannot perform a required operation and the change is explicitly justified.

---

# 5. Repository Structure

Expected structure:

```text
/
├── AGENTS.md
├── README.md
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── types/
│   └── public/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── migrations/
│   └── tests/
│
├── media/
│   ├── uploads/
│   └── evidence/
│
└── docs/
```

Keep frontend and backend concerns separated.

---

# 6. Architecture Rules

## Frontend Responsibilities

The frontend owns:

- User interface
- Image upload
- Video upload
- Camera interaction
- Media preview
- Progress states
- Results visualization
- Dashboard
- Filters
- Map visualization
- Report details
- Status controls

The frontend MUST NOT own authoritative:

- Severity
- Priority
- AI decisions
- Database state

---

## Backend Responsibilities

The backend owns:

- API contracts
- File validation
- Image processing
- Video processing
- Frame sampling
- Nemotron orchestration
- AI output validation
- Severity calculation
- Priority calculation
- Report persistence
- Status transition validation
- Error handling

The backend is the source of truth for business logic.

---

# 7. AI Architecture Rules

Never scatter Nemotron calls throughout the application.

Use a dedicated service boundary:

```text
API
 ↓
Analysis Service
 ↓
AI Service
 ↓
Nemotron
```

Recommended location:

```text
backend/app/services/ai_service.py
```

The rest of the backend should call the AI service interface rather than directly depending on provider-specific implementation details.

This allows the model/inference configuration to change without rewriting the application.

---

# 8. AI Output Contract

AI output MUST be structured.

Target schema:

```json
{
  "issue_detected": true,
  "issue_type": "pothole",
  "confidence": 0.94,
  "severity": "HIGH",
  "priority": "P2",
  "description": "Large pothole detected on road surface.",
  "recommended_action": "Schedule road repair urgently."
}
```

The backend MUST validate AI output using Pydantic or equivalent schema validation.

Never store unrestricted model output directly as an infrastructure report.

---

# 9. Supported Issue Types

Initial supported categories:

```text
pothole
damaged_road
broken_streetlight
overflowing_drain
unknown
```

Use consistent machine-readable identifiers.

Do not create arbitrary category names in different parts of the codebase.

---

# 10. Severity Rules

Supported values:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Meaning:

```text
LOW      → Minor issue
MEDIUM   → Requires maintenance
HIGH     → Significant concern
CRITICAL → Immediate attention required
```

AI may recommend severity, but the backend must validate and normalize it.

---

# 11. Priority Rules

Priority mapping:

```text
CRITICAL → P1
HIGH     → P2
MEDIUM   → P3
LOW      → P4
```

Priority MUST be determined server-side.

Do not blindly trust priority sent by the frontend.

---

# 12. Image Processing Rules

Image flow:

```text
Upload
 ↓
Validate
 ↓
Preprocess if necessary
 ↓
Nemotron / AI
 ↓
Validate structured output
 ↓
Severity
 ↓
Priority
 ↓
Report
```

Validate:

- MIME type
- File size
- Basic image integrity
- Required request fields

Do not unnecessarily resize or transform images unless required by the inference pipeline.

---

# 13. Video Processing Rules

Video flow:

```text
Upload
 ↓
Validate
 ↓
Read Metadata
 ↓
Frame Sampling
 ↓
AI Analysis
 ↓
Timestamp Findings
 ↓
Temporal Aggregation
 ↓
Severity / Priority
 ↓
Report
```

## Important

Do NOT analyze every frame of a video by default.

Use configurable sampling.

Example:

```text
VIDEO
 ↓
Every N seconds
 ↓
Selected frames
 ↓
AI
```

The sampling interval must be configurable through backend configuration.

---

# 14. Video Aggregation Rules

The same physical issue can appear in many consecutive frames.

Bad:

```text
Frame 1 → Pothole #1
Frame 2 → Pothole #2
Frame 3 → Pothole #3
Frame 4 → Pothole #4
```

Preferred:

```text
Frame 1 → Pothole
Frame 2 → Pothole
Frame 3 → Pothole
Frame 4 → Pothole

        ↓

One Pothole Finding
```

For MVP, temporal proximity and simple matching are sufficient.

Do not implement complex object tracking unless the core MVP is already complete.

---

# 15. Infrastructure Report

Use one consistent report model.

Suggested fields:

```text
id
media_type
media_url
issue_type
confidence
severity
priority
description
recommended_action
latitude
longitude
location_name
video_timestamp
status
created_at
updated_at
```

---

# 16. Report Lifecycle

Allowed lifecycle:

```text
REPORTED
   ↓
AI_ANALYZED
   ↓
PRIORITIZED
   ↓
ASSIGNED
   ↓
IN_PROGRESS
   ↓
RESOLVED
```

Backend must validate status transitions.

---

# 17. API Rules

Required endpoints:

```text
GET    /api/health

POST   /api/analyze/image
POST   /api/analyze/video

GET    /api/analysis/{analysis_id}

POST   /api/reports
GET    /api/reports
GET    /api/reports/{report_id}

PATCH  /api/reports/{report_id}/status
```

Use a consistent response envelope.

Success:

```json
{
  "success": true,
  "data": {}
}
```

Error:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_MEDIA",
    "message": "Unsupported media format."
  }
}
```

Do not invent new response structures for individual endpoints without a clear reason.

---

# 18. Frontend API Rules

Centralize backend calls.

Recommended:

```text
frontend/lib/api.ts
```

Use typed functions such as:

```text
analyzeImage()
analyzeVideo()
getAnalysis()
createReport()
getReports()
getReport()
updateReportStatus()
checkHealth()
```

Do not scatter raw `fetch()` calls throughout UI components.

---

# 19. Environment and Secrets

Never hard-code:

- API keys
- Database passwords
- Nemotron credentials
- Provider secrets

Frontend:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend:

```env
DATABASE_URL=...
AI_PROVIDER=nemotron
AI_MODEL=...
AI_API_KEY=...
```

`.env` files must not be committed.

---

# 20. Database Rules

Use:

- PostgreSQL
- SQLAlchemy
- Alembic

Database migrations must be reproducible.

Do not manually modify production schema without a migration.

For the hackathon MVP, media files may remain in local/object storage while PostgreSQL stores their references.

---

# 21. Error Handling

Every major operation must fail gracefully.

Handle:

```text
Invalid media
File too large
Unsupported format
AI failure
Video processing failure
Database failure
Missing location
Network failure
Invalid AI response
Missing report
```

Never expose:

- Stack traces
- Internal provider details
- Secrets
- Database credentials

to end users.

---

# 22. Reliability / Demo Fallback

Because this is a time-constrained hackathon:

If Nemotron or another external dependency fails, the application should have a controlled fallback path for demonstration.

Possible fallback:

```text
AI unavailable
     ↓
Fallback analysis/demo fixture
     ↓
Continue report workflow
```

Fallback logic must be clearly separated from the real AI path.

Do not fake AI results silently in production mode.

---

# 23. UI/UX Rules

The user must always know what the system is doing.

Use states:

```text
IDLE
UPLOADING
PROCESSING
ANALYZING
GENERATING_REPORT
COMPLETE
ERROR
```

For video, progress should be visible.

Do not leave the user on an indefinite spinner.

---

# 24. Dashboard Requirements

Dashboard must contain:

### Summary

```text
Total Issues
Critical
High
Open
Resolved
```

### Reports

```text
ID
Issue
Type
Location
Severity
Priority
Status
```

### Filters

```text
Issue Type
Severity
Priority
Status
Media Type
Location
```

### Details

- Original media/evidence
- AI analysis
- Confidence
- Severity
- Priority
- Location
- Recommended action
- Status

---

# 25. Location Rules

Location may come from:

1. Browser/device GPS.
2. User input.
3. Map selection.
4. Media metadata where available.

GPS is optional.

If GPS is unavailable:

```text
GPS unavailable
     ↓
Manual location
```

Do not block report creation solely because GPS is unavailable.

---

# 26. Security Rules

At minimum:

- Validate file MIME type.
- Validate file size.
- Sanitize filenames.
- Use safe temporary paths.
- Never expose secrets.
- Validate all AI output.
- Do not trust client severity/priority.
- Restrict CORS to known origins.
- Avoid arbitrary file execution.
- Clean temporary media after processing when safe.

---

# 27. Performance Rules

Optimize for the hackathon MVP.

### Image

Process immediately where possible.

### Video

Sample frames instead of processing every frame.

### Long-running jobs

Use analysis IDs and polling if synchronous processing becomes too slow.

### Database

Avoid unnecessary queries.

### Frontend

Use server-state caching/query management where useful.

---

# 28. Coding Standards

## General

- Prefer readable code over clever code.
- Keep functions small and focused.
- Use descriptive names.
- Add types to public interfaces.
- Avoid duplicated business logic.
- Keep configuration centralized.
- Avoid unnecessary dependencies.

## Python

- Use type hints.
- Use Pydantic schemas for API contracts.
- Keep routes thin.
- Put business logic in services.
- Use SQLAlchemy models for persistence.

Preferred:

```text
Route
 ↓
Service
 ↓
Repository/DB
```

Avoid putting large business logic directly inside route functions.

## TypeScript

- Use strict typing.
- Avoid `any` unless unavoidable.
- Keep API types centralized.
- Use reusable components.
- Keep UI components focused.

---

# 29. Testing Rules

Test critical paths first.

Minimum backend tests:

```text
Health
Image analysis
Video analysis
Report creation
Report retrieval
Status update
Invalid media
Invalid AI output
```

Minimum frontend verification:

```text
Image upload
Video upload
Analysis loading
Result rendering
Dashboard
Filters
Status update
Error state
```

Always run an end-to-end test before demo freeze.

---

# 30. Development Order

Agents MUST follow this dependency order unless there is a strong reason not to:

```text
1. Project Setup
      ↓
2. Frontend + Backend Skeleton
      ↓
3. Database
      ↓
4. API Contracts
      ↓
5. AI Service Interface
      ↓
6. Image Analysis
      ↓
7. Severity + Priority
      ↓
8. Image UI
      ↓
9. Video Processing
      ↓
10. Video UI
      ↓
11. Reports
      ↓
12. Dashboard
      ↓
13. Location
      ↓
14. Status Lifecycle
      ↓
15. Error Handling
      ↓
16. Testing
      ↓
17. Demo Freeze
```

---

# 31. Three-Hour Hackathon Priority

## 0–20 minutes

```text
Repository
Frontend
Backend
Database
```

## 20–60 minutes

```text
API contracts
Nemotron service
Image analysis
Severity
Priority
```

Target:

```text
IMAGE → AI → RESULT
```

## 60–105 minutes

```text
Video metadata
Frame sampling
Video AI
Timestamping
Aggregation
```

Target:

```text
VIDEO → FRAMES → AI → FINDINGS
```

## 105–135 minutes

```text
Dashboard
Reports
Filters
Results UI
```

Target:

```text
RESULT → REPORT → DASHBOARD
```

## 135–155 minutes

```text
Location
Status lifecycle
```

## 155–170 minutes

```text
Error handling
Loading states
UI polish
```

## 170–180 minutes

```text
End-to-end test
Demo freeze
```

---

# 32. Scope Control

DO NOT prioritize these before the MVP works:

- Live CCTV streaming
- Full object tracking
- Advanced predictive maintenance
- Multi-city deployment
- Mobile app
- Complex GIS analytics
- Custom model training
- Large-scale distributed processing
- Full authentication/RBAC

These are future enhancements unless the core workflow is already complete.

---

# 33. Definition of Done

The system is considered MVP-complete when all of the following work:

```text
[ ] Image upload
[ ] Video upload
[ ] Image AI analysis
[ ] Video frame analysis
[ ] Issue classification
[ ] Confidence
[ ] Severity
[ ] Priority
[ ] Video timestamps
[ ] Repeated finding aggregation
[ ] Location
[ ] Report creation
[ ] Dashboard
[ ] Filters
[ ] Status updates
[ ] Error handling
[ ] End-to-end demo
```

---

# 34. Agent Behavior

When implementing a task:

1. Read the existing code before modifying it.
2. Check the relevant architecture/documentation.
3. Identify dependencies.
4. Make the smallest coherent implementation.
5. Do not rewrite unrelated modules.
6. Preserve existing API contracts.
7. Add or update tests where practical.
8. Run the relevant checks.
9. Fix errors before moving to the next task.
10. Clearly report what changed.

---

# 35. Change Safety Rules

Before modifying an existing API:

```text
Check:
- Frontend consumers
- Backend consumers
- Type definitions
- Tests
- Documentation
```

Do not silently change:

- Endpoint names
- JSON field names
- Enum values
- Database fields
- Status names

If a breaking change is necessary, update all consumers in the same task.

---

# 36. AI Prompting Rules

Prompts sent to Nemotron should:

- Define the supported issue categories.
- Request structured JSON.
- Require confidence.
- Require concise evidence-based descriptions.
- Avoid unsupported assumptions.
- Clearly distinguish visible evidence from inference.
- Request recommended action separately from observation.

The AI should not invent:

- Locations
- Damage that is not visible
- Exact measurements not available from the evidence
- Official municipal information
- False certainty

---

# 37. Final Product Principle

The product is NOT merely:

```text
Image Classifier
```

It is:

```text
Evidence
  ↓
AI Detection
  ↓
Classification
  ↓
Severity
  ↓
Priority
  ↓
Location
  ↓
Actionable Report
  ↓
Monitoring Dashboard
```

The final demonstration must make this complete chain obvious.

---

# 38. Final Agent Rule

## Build the smallest reliable system that demonstrates the complete value proposition.

Priority order:

```text
WORKING END-TO-END MVP
        >
RELIABLE DEMO
        >
CORRECT AI INTEGRATION
        >
GOOD UX
        >
ADVANCED FEATURES
```

Do not sacrifice the working image + video workflow for unnecessary complexity.
