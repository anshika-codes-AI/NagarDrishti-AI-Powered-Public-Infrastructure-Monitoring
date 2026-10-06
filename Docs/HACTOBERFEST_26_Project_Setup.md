# Project Setup Document

## AI-Powered Public Infrastructure Monitoring
### HACTOBERFEST '26

---

## 1. Objective

Set up a clean full-stack repository for a hackathon MVP containing:

- Next.js frontend
- FastAPI backend
- PostgreSQL database
- Nemotron AI integration
- Image analysis
- Video frame processing
- Infrastructure reporting dashboard

The setup must be simple enough to run locally and structured enough for Nemotron to implement task-by-task.

---

# 2. Repository Structure

```text
infrastructure-monitoring/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── types/
│   ├── public/
│   ├── package.json
│   └── .env.local
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
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
├── media/
│   ├── uploads/
│   └── evidence/
│
├── docs/
│
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

# 3. Frontend Setup

## 3.1 Requirements

Recommended environment:

```text
Node.js
npm
Git
```

Create the application:

```bash
npx create-next-app@latest frontend --typescript --tailwind --eslint --app
```

Enter directory:

```bash
cd frontend
```

Install UI dependencies as required:

```bash
npm install
```

Add additional packages for the implementation:

```bash
npm install @tanstack/react-query
npm install lucide-react
```

Add the chosen shadcn/ui components during implementation.

---

# 4. Frontend Environment

Create:

```text
frontend/.env.local
```

Add:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Do not put Nemotron/provider secrets in this file.

---

# 5. Backend Setup

## 5.1 Requirements

Recommended:

```text
Python 3.11+
pip
virtualenv
Git
FFmpeg
PostgreSQL
```

Create environment:

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

---

# 6. Backend Dependencies

Create:

```text
requirements.txt
```

Initial dependencies:

```text
fastapi
uvicorn[standard]
pydantic
pydantic-settings
python-multipart
sqlalchemy
alembic
psycopg2-binary
opencv-python
httpx
python-dotenv
```

Install:

```bash
pip install -r requirements.txt
```

Add the exact Nemotron client/inference dependency according to the available Nemotron environment.

Do not hard-code a provider-specific package until the actual inference interface is confirmed.

---

# 7. Backend Environment

Create:

```text
backend/.env
```

Example:

```env
APP_ENV=development
HOST=0.0.0.0
PORT=8000

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/infrastructure_monitoring

AI_PROVIDER=nemotron
AI_MODEL=<configured-nemotron-model>
AI_BASE_URL=<configured-if-required>
AI_API_KEY=<configured-if-required>

MAX_IMAGE_SIZE_MB=10
MAX_VIDEO_SIZE_MB=100
VIDEO_FRAME_SAMPLE_INTERVAL=2
```

Secrets must remain local and must never be committed.

---

# 8. Database Setup

Create a PostgreSQL database:

```text
infrastructure_monitoring
```

Example local connection:

```text
postgresql://postgres:postgres@localhost:5432/infrastructure_monitoring
```

Initialize SQLAlchemy and Alembic.

Initial model:

```text
InfrastructureReport
```

Core fields:

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

# 9. Backend Application Entry Point

Create:

```text
backend/app/main.py
```

Responsibilities:

- Create FastAPI app.
- Configure CORS.
- Register API routers.
- Configure exception handling.
- Configure startup/shutdown behavior.

Initial API:

```text
GET /api/health
```

Run:

```bash
uvicorn app.main:app --reload --port 8000
```

---

# 10. CORS

During local development allow the frontend origin:

```text
http://localhost:3000
```

Production must use an explicit allowed-origin list.

Do not use unrestricted CORS in production.

---

# 11. Frontend-Backend Connection Test

Start backend:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Start frontend:

```bash
cd frontend
npm run dev
```

Open:

```text
http://localhost:3000
```

Verify:

```text
Frontend
   ↓
GET /api/health
   ↓
Backend
   ↓
healthy
```

---

# 12. Media Storage

For the hackathon MVP:

```text
media/
  uploads/
  evidence/
```

Use temporary/local storage for development.

The database should store media references rather than binary media where practical.

Production storage can later be replaced with object storage.

---

# 13. Git Setup

Initialize:

```bash
git init
```

Create `.gitignore`:

```text
node_modules/
.next/
.env
.env.local
.venv/
__pycache__/
*.pyc
media/uploads/*
media/evidence/*
```

Never commit:

```text
AI API keys
database passwords
.env files
large uploaded videos
private credentials
```

---

# 14. Docker Option

A `docker-compose.yml` can provide PostgreSQL for consistent local development.

Core services:

```text
postgres
```

Frontend/backend may run locally during the 3-hour hackathon to reduce setup complexity.

---

# 15. Initial Verification Checklist

### Frontend

```text
[ ] Next.js starts
[ ] TypeScript compiles
[ ] Tailwind works
[ ] API URL configured
```

### Backend

```text
[ ] FastAPI starts
[ ] Health endpoint works
[ ] CORS works
[ ] Environment variables load
```

### Database

```text
[ ] PostgreSQL starts
[ ] Database exists
[ ] SQLAlchemy connects
[ ] Migration runs
```

### Media

```text
[ ] Image upload path exists
[ ] Video upload path exists
[ ] Evidence path exists
```

### AI

```text
[ ] Nemotron configuration exists
[ ] AI service interface exists
[ ] Credentials are not hard-coded
```

---

# 16. Definition of Setup Complete

The project setup is complete when:

```text
Frontend
   ↕
FastAPI
   ↕
PostgreSQL
   ↕
AI Service Interface
```

all start successfully and the repository can be cloned and configured without modifying source code for secrets.

---

# 17. First Run Sequence

```bash
# Terminal 1
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

# Terminal 2
cd frontend
npm run dev
```

Then open:

```text
http://localhost:3000
```

---

# 18. Setup Principle

Do not over-engineer the infrastructure during the hackathon.

Priority:

```text
Working local environment
        >
Clean architecture
        >
Production infrastructure
```

The first goal is to make the complete image/video workflow executable locally.
