IMPLEMENTATION PLAN
AI-Powered Public Infrastructure Monitoring
HACTOBERFEST '26

# 1. Purpose

Build a web-based AI-powered public infrastructure monitoring system capable of analyzing both images and videos to automatically detect infrastructure problems, classify the detected problem, estimate severity, assign an actionable priority, identify or attach location information where available, generate a structured maintenance report, and display and manage issues through a monitoring dashboard.
The source problem statement identifies public infrastructure issues such as potholes, damaged roads, broken streetlights, and overflowing drains and calls for automatic detection, classification, and prioritization for faster action.

# 2. Product Vision

Turn infrastructure images and field videos into actionable maintenance intelligence.
Instead of manually inspecting every image or video, the system uses AI to analyze submitted evidence and convert it into a structured infrastructure report.
Core flow: Image/Video -> AI Analysis -> Issue Detection -> Classification -> Severity -> Priority -> Location -> Maintenance Report -> Dashboard -> Action

# 3. MVP Scope


## 3.1 Image Inspection

The user uploads or captures an image. The system analyzes it and produces an infrastructure report containing issue type, confidence, severity, priority, description, and recommended action.

## 3.2 Video Inspection

The user uploads a video. The backend samples selected frames instead of processing every frame unnecessarily, analyzes those frames, tracks timestamps, aggregates repeated detections, and produces consolidated findings.

# 4. Supported Infrastructure Categories

- Pothole
- Damaged Road
- Broken Streetlight
- Overflowing Drain
- Unknown / Other

# 5. Image Processing Pipeline

User -> Upload / Camera Capture -> Validate Image -> Preprocess -> AI Vision Analysis -> Structured AI Response -> Validate AI Response -> Severity Engine -> Priority Engine -> Create Report -> Dashboard

# 6. Video Processing Pipeline

Video Upload -> Video Validation -> Read Metadata -> Frame Sampling -> Selected Frames -> AI Analysis -> Frame-Level Detections -> Temporal Aggregation -> Duplicate Issue Grouping -> Final Video Findings -> Severity + Priority -> Report

## 6.1 Frame Sampling

The system will not send every video frame to the AI model. A configurable sampling interval will balance accuracy, processing speed, and compute cost.

## 6.2 Frame-Level Analysis

Each selected frame should return the timestamp, issue detection state, issue type, confidence, and severity.

## 6.3 Temporal Aggregation

Repeated detections of the same physical issue across consecutive frames should be consolidated into a single infrastructure report. The MVP may use temporal proximity and simple matching heuristics; advanced object tracking remains a future enhancement.

# 7. AI Layer -- Nemotron

Nemotron will be used as the primary reasoning/intelligence layer wherever the available model configuration supports the required input. The AI layer should convert visual evidence into structured output rather than unrestricted text.
AI responsibilities: observation, issue classification, confidence estimation, severity reasoning, and recommended action.
Target output schema: {"issue_detected": true, "issue_type": "pothole", "confidence": 0.94, "severity": "HIGH", "priority": "P2", "description": "...", "recommended_action": "..."}
The backend must validate the AI response before sending it to the frontend.

# 8. Severity Engine

Severity represents how serious the infrastructure problem is.
The system can combine AI assessment with deterministic rules so the result remains predictable and explainable.

# 9. Priority Engine

Severity is converted into an operational priority.

# 10. Location System

Each report should contain location information whenever available.
- Browser/device GPS
- User-provided location
- Map selection
- Optional location metadata associated with uploaded media
If GPS is unavailable, the application must allow manual location input.

# 11. Infrastructure Report

Every detected issue becomes a standardized report containing: Report ID, media type, media reference, issue type, confidence, severity, priority, description, recommended action, location, status, timestamp, created_at, and updated_at.
For video-generated reports, the report should additionally retain the relevant video timestamp and evidence frame.

# 12. Monitoring Dashboard

The dashboard provides a central view of all infrastructure issues.
- Summary cards: Total Issues, Critical, High, Open, Resolved
- Issue table with issue, type, location, severity, priority, and status
- Filters for issue type, severity, priority, status, media type, and location

# 13. Video Evidence Viewer

For video-generated reports, the dashboard should show the source video, issue timestamp, evidence frame, issue type, severity, and priority.

# 14. Issue Lifecycle

REPORTED -> AI ANALYZED -> PRIORITIZED -> ASSIGNED -> IN PROGRESS -> RESOLVED

# 15. Recommended Technology Stack


## 15.1 Frontend

Next.js, TypeScript, Tailwind CSS, shadcn/ui
- Image upload
- Video upload
- Camera interface
- Analysis progress
- Results
- Dashboard
- Filters
- Map
- Report details
- Video evidence

## 15.2 Backend

Python, FastAPI, Pydantic
- Media upload
- Image processing
- Video frame extraction
- AI orchestration
- Response validation
- Severity engine
- Priority engine
- Reports
- Dashboard APIs

## 15.3 Video Processing

OpenCV and FFmpeg where required.

## 15.4 Database

PostgreSQL
Primary entity: InfrastructureReport
Suggested fields: id, media_type, media_url, issue_type, confidence, severity, priority, description, recommended_action, latitude, longitude, location_name, video_timestamp, status, created_at, updated_at.

# 16. API Architecture

- GET /api/health -- health check
- POST /api/analyze/image -- analyze image
- POST /api/analyze/video -- analyze video
- GET /api/analysis/{id} -- get analysis
- POST /api/reports -- create report
- GET /api/reports -- get reports
- GET /api/reports/{id} -- get report
- PATCH /api/reports/{id}/status -- update status

# 17. Three-Hour Development Schedule


# 18. Demo Strategy


## 18.1 Image Demo

Upload a road image -> AI detects the infrastructure issue -> display confidence, severity, priority, and recommended action -> create the report.

## 18.2 Video Demo

Upload a short road inspection video -> sample frames -> analyze frames -> detect multiple issues -> show timestamps -> aggregate repeated detections -> display findings on the dashboard.

# 19. Reliability & Fallback Strategy

- AI failure: use a fallback analysis/predefined demo dataset so the demo can continue.
- GPS failure: allow manual location.
- Video processing failure: display extracted/preloaded evidence frames where appropriate.
- Database failure: maintain a lightweight in-memory fallback for the hackathon prototype.

# 20. Security & Validation

The backend should validate file type, file size, image dimensions, video format, request fields, and AI response schema.
Raw AI output must never be trusted directly. The pipeline is: AI Output -> Pydantic Validation -> Business Rules -> Database -> Frontend.

# 21. Performance Strategy

- Process images immediately.
- Use controlled video frame sampling instead of processing every frame.
- Use structured AI prompts and constrained output.
- Use asynchronous processing where appropriate.
- Show progress states: Uploading -> Processing -> Analyzing -> Generating Report -> Complete.

# 22. Out of Scope for MVP

- Full-scale object tracking
- Live CCTV streaming
- Multi-city deployment
- Advanced predictive maintenance
- Complex GIS analytics
- Mobile application
- Large-scale distributed processing
- Training a new computer-vision model from scratch

# 23. Success Criteria


## 23.1 Image

- Upload image
- Detect infrastructure issue
- Classify issue
- Generate confidence
- Determine severity
- Determine priority
- Generate report

## 23.2 Video

- Upload video
- Extract frames
- Analyze selected frames
- Detect multiple issues
- Show timestamps
- Aggregate repeated detections
- Generate report

## 23.3 Dashboard

- Display issues
- Filter issues
- Show severity
- Show priority
- Show location
- Update status

# 24. Final Architecture

User -> Image/Video Input -> Image Analysis or Video Frame Extraction -> Nemotron AI Analysis -> Structured Analysis -> Classification + Confidence -> Severity Engine -> Priority Engine -> Location System -> Report Generator -> PostgreSQL -> REST API -> Monitoring Dashboard -> Maintenance Action

# 25. Final Implementation Principle

Build the complete workflow first. Add intelligence and visual polish second.
The primary priority is an end-to-end working system and reliable demo. A stable image + video workflow is more valuable than many partially implemented advanced features.
Final product statement: “Give us an image or video of public infrastructure, and our system automatically turns that raw evidence into a prioritized maintenance action.”

| Level | Meaning |
| --- | --- |
| LOW | Minor issue |
| MEDIUM | Requires maintenance |
| HIGH | Significant concern |
| CRITICAL | Immediate attention required |


| Severity | Priority |
| --- | --- |
| CRITICAL | P1 -- Immediate action |
| HIGH | P2 -- Urgent maintenance |
| MEDIUM | P3 -- Scheduled maintenance |
| LOW | P4 -- Monitor / routine maintenance |


| Time | Work |
| --- | --- |
| 0-20 Minutes -- Foundation | Repository setup, frontend setup, FastAPI setup, environment configuration, basic API connection, base UI. |
| 20-60 Minutes -- Image MVP | Image upload, AI analysis, structured response, classification, severity, priority, and result page. |
| 60-105 Minutes -- Video MVP | Video upload, metadata extraction, frame sampling, frame analysis, timestamp tracking, result aggregation, evidence frames. |
| 105-135 Minutes -- Dashboard | Summary cards, reports table, severity and priority badges, status, filters, report details. |
| 135-155 Minutes -- Location + Lifecycle | GPS/manual location, map, report status, and Open -> Assigned -> In Progress -> Resolved. |
| 155-170 Minutes -- Polish | Loading states, progress indicators, error handling, empty states, responsive UI, and visual hierarchy. |
| 170-180 Minutes -- Final Demo Test | End-to-end image and video testing, bug fixes, and demo freeze. |
