@echo off
cd /d "A:\AI-Powered Public Infra Monitoring\backend"
python -m uvicorn app.main:app --port 8000 --host 127.0.0.1