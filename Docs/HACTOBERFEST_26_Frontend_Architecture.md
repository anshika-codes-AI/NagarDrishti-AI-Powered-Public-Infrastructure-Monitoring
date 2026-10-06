FRONTEND ARCHITECTURE
AI-Powered Public Infrastructure Monitoring
HACTOBERFEST '26

# 1. Architecture Objective

Design a fast, clear, responsive web interface that supports both image and video infrastructure inspection, presents AI analysis transparently, and provides a municipal-style monitoring dashboard.

# 2. Frontend Technology Stack

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- React Query / TanStack Query for server state
- Leaflet or equivalent map component for location visualization

# 3. High-Level Frontend Architecture

Browser -> Next.js UI -> Feature Components -> API Client -> FastAPI Backend -> AI/Processing Services
The frontend is responsible for presentation, user interaction, upload handling, progress states, result visualization, dashboard filtering, map display, and report status updates. AI inference and business rules remain backend responsibilities.

# 4. Application Structure

- Home / Inspection page -- choose Image or Video input.
- Image Analysis page -- upload/capture image, submit, and display analysis.
- Video Analysis page -- upload video, show processing progress, timestamps, and findings.
- Results page -- show issue type, confidence, severity, priority, description, location, and recommended action.
- Dashboard -- aggregate infrastructure reports with summary cards, filters, table, and map.
- Report Details -- complete report and media evidence.
- About / Project page -- explain the solution and workflow.

# 5. Suggested Folder Structure

src/
  app/
    page.tsx
    analyze/image/page.tsx
    analyze/video/page.tsx
    dashboard/page.tsx
    reports/[id]/page.tsx
  components/
    upload/
    analysis/
    dashboard/
    reports/
    map/
    ui/
  lib/
    api.ts
    validators.ts
    utils.ts
  hooks/
    useImageAnalysis.ts
    useVideoAnalysis.ts
    useReports.ts
  types/
    analysis.ts
    report.ts
    api.ts

# 6. Input Architecture


## 6.1 Image Input

- File upload
- Camera capture where browser permissions allow
- Image preview
- File validation
- Upload progress
- Analysis status

## 6.2 Video Input

- Video upload
- Video preview
- File validation
- Upload progress
- Processing progress
- Analysis progress
- Findings with timestamps

# 7. Shared Analysis State

The UI should represent a common lifecycle for both media types:
IDLE -> UPLOADING -> PROCESSING -> ANALYZING -> GENERATING REPORT -> COMPLETE / ERROR

# 8. Results UI


# 9. Dashboard Architecture

- Summary cards: total, critical, high, open, resolved
- Issue table
- Severity and priority indicators
- Status controls
- Filters: issue type, severity, priority, status, media type, location
- Map visualization
- Report detail navigation

# 10. Component Architecture

Core reusable components:
- MediaUploader
- ImagePreview
- VideoPreview
- AnalysisProgress
- AnalysisResultCard
- SeverityBadge
- PriorityBadge
- IssueStatusBadge
- ReportTable
- ReportFilters
- SummaryCards
- InfrastructureMap
- EvidenceFrame
- ReportDetails

# 11. API Client Layer

All backend communication should go through a centralized API client rather than scattering fetch calls throughout UI components.
- POST /api/analyze/image
- POST /api/analyze/video
- GET /api/analysis/{id}
- POST /api/reports
- GET /api/reports
- GET /api/reports/{id}
- PATCH /api/reports/{id}/status

# 12. Data Models

Frontend TypeScript types should mirror the backend contracts.
AnalysisResult: issue_detected, issue_type, confidence, severity, priority, description, recommended_action, location, video_timestamp, evidence_frame.
InfrastructureReport: id, media_type, media_url, issue_type, confidence, severity, priority, description, recommended_action, location, status, timestamps.

# 13. UX and Error Handling

- Reject unsupported media types before upload.
- Display file-size errors clearly.
- Never leave the user on an indefinite loading screen.
- Show retry action on failed analysis.
- Handle missing GPS with manual location option.
- Handle AI uncertainty with an explicit low-confidence state.
- For video, show progress so processing does not appear frozen.

# 14. Responsive Design

- Desktop-first dashboard for judges/admin users.
- Mobile-friendly inspection/upload experience.
- Responsive cards and tables.
- Touch-friendly upload and status controls.

# 15. Frontend Security

- Do not expose AI/provider secrets in browser code.
- Use environment variables only for public-safe configuration.
- Validate file metadata before upload.
- Do not trust client-side severity or priority; backend remains authoritative.

# 16. Frontend Demo Flow

Home -> Select Image/Video -> Upload -> Processing -> AI Result -> Severity/Priority -> Create Report -> Dashboard -> Open Report -> Update Status

# 17. Frontend Completion Criteria

- Image workflow works end-to-end.
- Video workflow works end-to-end.
- Analysis states are visible.
- Results are readable.
- Dashboard displays reports.
- Filters work.
- Location is shown when available.
- Video timestamps/evidence are visible.
- Status can be updated.
- Application remains usable on errors.

| Section | Displayed Information |
| --- | --- |
| Detection | Issue detected / no issue |
| Classification | Pothole, Damaged Road, Broken Streetlight, Overflowing Drain, Other |
| Confidence | AI confidence score |
| Severity | LOW / MEDIUM / HIGH / CRITICAL |
| Priority | P1 / P2 / P3 / P4 |
| Description | Human-readable explanation |
| Action | Recommended maintenance action |
| Location | Name + coordinates when available |
| Video Evidence | Timestamp + evidence frame for video |
