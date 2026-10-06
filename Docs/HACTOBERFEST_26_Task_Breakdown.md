# Task Breakdown Document

## AI-Powered Public Infrastructure Monitoring
### HACTOBERFEST '26

---

## 1. Objective

Break the implementation into small, independently executable tasks that can be assigned to developers or given sequentially to Nemotron.

The system supports:

- Image analysis
- Video analysis
- Infrastructure classification
- Severity
- Priority
- Location
- Reports
- Dashboard

---

# 2. Task Rules

1. Complete foundational tasks before dependent tasks.
2. Keep frontend and backend contracts synchronized.
3. Test every major task immediately.
4. Do not add non-MVP features before the core flow works.
5. Keep Nemotron integration behind a dedicated service interface.
6. Treat backend validation and business rules as authoritative.

---

# 3. Phase 0 — Repository and Setup

### TASK-001 — Initialize Repository

**Goal:** Create the root repository.

Deliverables:

```text
frontend/
backend/
docs/
media/
README.md
.gitignore
```

Acceptance:

- Git repository initialized.
- Folder structure exists.

---

### TASK-002 — Initialize Next.js

Deliverables:

- Next.js app
- TypeScript
- Tailwind
- App Router

Acceptance:

```bash
npm run dev
```

starts successfully.

---

### TASK-003 — Initialize FastAPI

Deliverables:

- FastAPI app
- `/api/health`
- CORS
- environment configuration

Acceptance:

```bash
uvicorn app.main:app --reload
```

starts successfully.

---

### TASK-004 — Database Setup

Deliverables:

- PostgreSQL database
- SQLAlchemy
- Alembic
- Initial report model

Acceptance:

- Database connection succeeds.
- Migration succeeds.

---

# 4. Phase 1 — Backend Foundation

### TASK-005 — API Response Contract

Implement:

```json
{
  "success": true,
  "data": {}
}
```

and:

```json
{
  "success": false,
  "error": {
    "code": "...",
    "message": "..."
  }
}
```

Acceptance:

- All APIs follow the same envelope.

---

### TASK-006 — Media Validation

Implement validation for:

- Image MIME type
- Video MIME type
- File size
- Filename
- Basic media integrity

Acceptance:

- Invalid media receives a controlled error.

---

### TASK-007 — Infrastructure Report Model

Implement:

```text
InfrastructureReport
```

Fields:

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

# 5. Phase 2 — Nemotron Integration

### TASK-008 — AI Service Interface

Create:

```text
services/ai_service.py
```

The rest of the backend should call an abstracted AI service rather than directly depending on provider-specific code.

Acceptance:

```text
backend → ai_service → Nemotron
```

---

### TASK-009 — Image AI Analysis

Input:

```text
Image
```

Output:

```text
issue_detected
issue_type
confidence
severity
description
recommended_action
```

Acceptance:

- One image produces validated structured JSON.

---

### TASK-010 — AI Output Validation

Create Pydantic schemas.

Acceptance:

- Invalid AI output is rejected or normalized.
- Raw AI text is never directly stored as a report.

---

# 6. Phase 3 — Severity and Priority

### TASK-011 — Severity Engine

Implement:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Acceptance:

- Every detected issue receives a valid severity.

---

### TASK-012 — Priority Engine

Implement:

```text
CRITICAL → P1
HIGH     → P2
MEDIUM   → P3
LOW      → P4
```

Acceptance:

- Priority is derived server-side.

---

# 7. Phase 4 — Image Workflow

### TASK-013 — Image Analysis Endpoint

Implement:

```http
POST /api/analyze/image
```

Acceptance:

```text
Image
 ↓
Validation
 ↓
AI
 ↓
Severity
 ↓
Priority
 ↓
Result
```

---

### TASK-014 — Image Report Creation

Implement:

```http
POST /api/reports
```

Acceptance:

- Image analysis can become a persistent report.

---

# 8. Phase 5 — Video Workflow

### TASK-015 — Video Metadata

Extract:

- Duration
- FPS
- Width
- Height
- Frame count

Acceptance:

- Metadata is available before processing.

---

### TASK-016 — Frame Sampling

Implement configurable frame sampling.

Example:

```text
VIDEO
 ↓
Every N seconds
 ↓
Selected frames
```

Acceptance:

- Video is not processed frame-by-frame unnecessarily.

---

### TASK-017 — Video AI Analysis

Send sampled frames to the AI service.

Each result must retain:

```text
timestamp
issue_type
confidence
severity
```

---

### TASK-018 — Temporal Aggregation

Group repeated detections of the same issue.

Example:

```text
00:08 Pothole
00:10 Pothole
00:12 Pothole
```

becomes:

```text
Pothole
Evidence: 00:08–00:12
```

Acceptance:

- Duplicate consecutive findings do not create unnecessary reports.

---

### TASK-019 — Video Analysis Endpoint

Implement:

```http
POST /api/analyze/video
```

Acceptance:

- Video upload produces timestamped findings.

---

# 9. Phase 6 — Location

### TASK-020 — Location Input

Support:

- Latitude
- Longitude
- Location name

Acceptance:

- GPS is optional.
- Manual location is possible.

---

### TASK-021 — Location Display

Return location information in report responses.

---

# 10. Phase 7 — Frontend Foundation

### TASK-022 — Application Shell

Create:

- Navbar
- Main layout
- Navigation
- Responsive structure

---

### TASK-023 — Image Upload UI

Implement:

- Drag/drop
- File selection
- Preview
- Upload
- Validation

Acceptance:

- User can select an image and submit it.

---

### TASK-024 — Video Upload UI

Implement:

- Video selection
- Preview
- File validation
- Upload
- Processing progress

---

# 11. Phase 8 — Analysis UI

### TASK-025 — Analysis Progress

States:

```text
UPLOADING
PROCESSING
ANALYZING
GENERATING REPORT
COMPLETE
ERROR
```

---

### TASK-026 — Analysis Result Card

Display:

```text
Issue
Confidence
Severity
Priority
Description
Recommended Action
```

---

### TASK-027 — Video Findings UI

Display:

```text
Timestamp
Issue
Severity
Priority
Evidence Frame
```

---

# 12. Phase 9 — Dashboard

### TASK-028 — Dashboard Summary

Cards:

```text
Total Issues
Critical
High
Open
Resolved
```

---

### TASK-029 — Reports Table

Columns:

```text
ID
Issue
Type
Location
Severity
Priority
Status
```

---

### TASK-030 — Dashboard Filters

Filters:

```text
Issue Type
Severity
Priority
Status
Media Type
Location
```

---

### TASK-031 — Report Details

Display:

- Original media
- AI result
- Severity
- Priority
- Location
- Recommended action
- Status
- Video timestamp/evidence where applicable

---

# 13. Phase 10 — Status Lifecycle

### TASK-032 — Status API

Implement:

```http
PATCH /api/reports/{id}/status
```

Allowed flow:

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

---

### TASK-033 — Status UI

Allow authorized dashboard users to update report status.

For the hackathon MVP, a full authentication system is optional and should not block the core workflow.

---

# 14. Phase 11 — Reliability

### TASK-034 — Error Handling

Handle:

- Invalid media
- AI failure
- Video processing failure
- Database failure
- Missing location
- Network failure

---

### TASK-035 — AI Fallback

Create a controlled fallback/demo path so the presentation does not completely fail if AI inference becomes unavailable.

---

### TASK-036 — Loading and Empty States

Add:

- Uploading state
- Processing state
- Empty dashboard
- No results
- Error state
- Retry action

---

# 15. Phase 12 — Testing

### TASK-037 — Backend API Tests

Test:

```text
Health
Image analysis
Video analysis
Reports
Status update
Invalid input
```

---

### TASK-038 — Image Test Set

Test at least:

```text
Pothole
Damaged road
Streetlight
Drain
Unknown
```

---

### TASK-039 — Video Test Set

Use short videos containing:

- One issue
- Multiple issues
- Repeated visibility of the same issue

---

### TASK-040 — End-to-End Test

Verify:

```text
Upload
 ↓
Analyze
 ↓
Classify
 ↓
Severity
 ↓
Priority
 ↓
Report
 ↓
Dashboard
 ↓
Status
```

for both image and video.

---

# 16. Three-Hour Priority Plan

## 0–20 min

Must finish:

```text
TASK-001
TASK-002
TASK-003
TASK-004
```

---

## 20–60 min

Focus:

```text
TASK-005
TASK-006
TASK-008
TASK-009
TASK-010
TASK-011
TASK-012
TASK-013
```

Goal:

**Working Image → AI → Result**

---

## 60–105 min

Focus:

```text
TASK-015
TASK-016
TASK-017
TASK-018
TASK-019
```

Goal:

**Working Video → Frames → AI → Findings**

---

## 105–135 min

Focus:

```text
TASK-022
TASK-026
TASK-028
TASK-029
TASK-030
TASK-031
```

Goal:

**Professional Dashboard**

---

## 135–155 min

Focus:

```text
TASK-020
TASK-021
TASK-032
TASK-033
```

Goal:

**Location + Status Lifecycle**

---

## 155–170 min

Focus:

```text
TASK-034
TASK-036
```

Goal:

**Reliability + UX polish**

---

## 170–180 min

Focus:

```text
TASK-040
```

Goal:

**Final end-to-end demo**

---

# 17. Priority Matrix

| Task | Priority | Must Have |
|---|---|---|
| Repository setup | P0 | Yes |
| FastAPI | P0 | Yes |
| Next.js | P0 | Yes |
| Database | P1 | Yes |
| Nemotron integration | P0 | Yes |
| Image analysis | P0 | Yes |
| Video analysis | P0 | Yes |
| Severity | P0 | Yes |
| Priority | P0 | Yes |
| Reports | P0 | Yes |
| Dashboard | P0 | Yes |
| Location | P1 | Yes |
| Status lifecycle | P1 | Yes |
| Advanced tracking | P3 | No |
| Live CCTV | P3 | No |
| Predictive maintenance | P3 | No |

---

# 18. Definition of Done

The project is ready for the hackathon demo when:

```text
[✓] Image upload works
[✓] Video upload works
[✓] Nemotron analysis works
[✓] Issue classification works
[✓] Severity works
[✓] Priority works
[✓] Video timestamps work
[✓] Reports are created
[✓] Dashboard works
[✓] Location can be attached
[✓] Status can be changed
[✓] Error handling exists
[✓] Complete demo works
```

---

# 19. Nemotron Execution Order

Nemotron should execute tasks in dependency order:

```text
1. Repository
      ↓
2. Frontend + Backend
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

# 20. Final Rule

**Do not build features in parallel that depend on unfinished contracts.**

First make this work:

```text
IMAGE → AI → RESULT
```

Then:

```text
VIDEO → FRAMES → AI → RESULT
```

Then:

```text
RESULT → REPORT → DASHBOARD
```

Finally:

```text
DASHBOARD → ACTION
```

This order minimizes integration risk during the 3-hour hackathon.
