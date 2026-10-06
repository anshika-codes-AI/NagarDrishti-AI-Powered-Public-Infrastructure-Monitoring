# AI-Powered Public Infrastructure Monitoring

**HACTOBERFEST '26** — Hackathon Project

## Project Purpose

A system that detects, classifies, and prioritizes public infrastructure issues (potholes, damaged roads, broken streetlights, overflowing drains) from uploaded images and videos. The AI-powered analysis determines severity and priority, attaches location information, and creates actionable reports displayed through a monitoring dashboard.

## Architecture

```text
Frontend (Next.js + TypeScript + Tailwind)
      ↓
API (FastAPI)
      ↓
Backend Services (SQLAlchemy + PostgreSQL)
      ↓
AI / Nemotron Analysis
      ↓
Media Processing (OpenCV + FFmpeg)
      ↓
Database (PostgreSQL)
      ↓
Reports / Dashboard
```

## Frontend

- **Framework**: Next.js 16 with App Router, TypeScript, Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: TanStack Query
- **Routing**: App Router (`app/` directory)
- **Entry Point**: `frontend/`

Start the frontend:

```bash
cd frontend
npm run dev
```

Open: http://localhost:3000

## Backend

- **Framework**: FastAPI (Python)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Database**: PostgreSQL
- **Media Processing**: OpenCV, FFmpeg
- **AI**: Nemotron structured JSON output

Start the backend:

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/health` | Service health check |
| POST | `/api/analyze/image` | Image analysis (coming soon) |
| POST | `/api/analyze/video` | Video analysis (coming soon) |
| GET | `/api/analysis/{id}` | Analysis status/result (coming soon) |
| POST | `/api/reports` | Create infrastructure report |
| GET | `/api/reports` | List reports |
| GET | `/api/reports/{id}` | Get single report |
| PATCH | `/api/reports/{id}/status` | Update lifecycle status |

Health endpoint response:

```json
{
  "success": true,
  "data": {
    "status": "healthy"
  }
}
```

### Environment Configuration

Create `backend/.env` from the `.env.example` template:

```
APP_ENV=development
HOST=0.0.0.0
PORT=8000
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/infrastructure_monitoring
AI_PROVIDER=nemotron
AI_MODEL=<configured-nemotron-model>
AI_API_KEY=<configured-if-required>
MAX_IMAGE_SIZE_MB=10
MAX_VIDEO_SIZE_MB=100
VIDEO_FRAME_SAMPLE_INTERVAL=2
```

Create `frontend/.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## AI / Nemotron

The backend integrates Nemotron as the structured AI analysis layer. AI output follows a strict JSON schema:

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

The backend validates all AI output using Pydantic schemas before persisting.

## Image + Video Support

- **Image**: Upload, validate, AI analysis, structured result
- **Video**: Upload, frame sampling (configurable interval), AI analysis per frame, temporal aggregation, timestamped findings

## Dashboard

The dashboard provides:

- **Summary**: Total Issues, Critical Issues, High Priority Issues, Open Issues, Resolved Issues
- **Issue List**: Filterable table of infrastructure reports
- **Filters**: Issue Type, Severity, Priority, Status, Media Type, Location
- **Map**: Geographic visualization of issues (when coordinates available)
- **Report Details**: Complete analysis view with media evidence and status controls

## How to Start (Full Stack)

1. **Backend**: `cd backend && python -m uvicorn app.main:app --reload --port 8000`
2. **Frontend**: `cd frontend && npm run dev`
3. **Open**: http://localhost:3000

Verify the health endpoint: `GET http://localhost:8000/api/health`

## Project Structure

```
/ (root)
├── AGENTS.md
├── README.md
├── .gitignore
├── backend/
│   ├── app/
│   │   ├── __init__.py       # FastAPI app with CORS, routes
│   │   ├── main.py           # Health endpoint
│   │   ├── api/              # API routers
│   │   ├── core/             # Core config, dependencies
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic services
│   │   ├── activities/       # Activity units
│   │   ├── dispatcher/       # Work coordination
│   │   └── utils/            # Utility functions
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment variables (no secrets)
│   ├── migrations/           # Alembic migrations
│   └── tests/                # Test files
├── frontend/
│   ├── app/                  # Next.js App Router
│   ├── components/           # React components
│   ├── lib/                  # API client, utilities
│   ├── types/                # TypeScript types
│   ├── public/               # Static assets
│   ├── package.json          # npm dependencies
│   └── .env.local            # Frontend environment
├── media/
│   ├── uploads/              # User-uploaded media (temp)
│   └── evidence/             # Extracted evidence frames
└── docs/                     # Project documentation
```

## Development

Follow the task breakdown in `AGENTS.md` for incremental implementation. The MVP priority order is:

1. Image upload + AI analysis
2. Video upload + frame sampling + AI analysis
3. Report creation + dashboard
4. Status lifecycle + filters + map

## License

HACTOBERFEST '26 — AI-Powered Public Infrastructure Monitoring