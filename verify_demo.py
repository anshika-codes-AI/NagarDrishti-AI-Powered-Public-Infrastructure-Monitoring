#!/usr/bin/env python
"""Quick verification script for the hackathon demo."""

import subprocess
import sys
import time
import json
import os

backend_dir = r"A:\AI-Powered Public Infra Monitoring\backend"
orig_dir = os.getcwd()
os.chdir(backend_dir)

results = []

try:
    # Start server
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000", "--host", "127.0.0.1"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    time.sleep(3)

    import urllib.request
    import urllib.error

    # Test 1: Health endpoint
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/health")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = json.loads(response.read().decode())
            ok = body.get("success") is True and body.get("data", {}).get("status") == "healthy"
            results.append(("GET /api/health", ok, body))
            print(f"  [{\"PASS\" if ok else \"FAIL\"}] GET /api/health")
    except Exception as e:
        results.append(("GET /api/health", False, str(e)))
        print(f"  [FAIL] GET /api/health: {e}")

    # Test 2: List reports
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/reports")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = json.loads(response.read().decode())
            ok = isinstance(body, list) or (body.get("success") is True)
            results.append(("GET /api/reports", ok, body))
            print(f"  [{\"PASS\" if ok else \"FAIL\"}] GET /api/reports")
    except Exception as e:
        results.append(("GET /api/reports", False, str(e)))
        print(f"  [FAIL] GET /api/reports: {e}")

    # Test 3: Create report (image)
    try:
        report_data = json.dumps({
            "media_type": "IMAGE",
            "issue_type": "pothole",
            "confidence": 0.95,
            "severity": "HIGH",
            "description": "Large pothole detected",
            "recommended_action": "Schedule repair"
        }).encode()
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/reports",
            data=report_data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            body = json.loads(response.read().decode())
            ok = body.get("success") is True and "data" in body
            results.append(("POST /api/reports (image)", ok, body))
            print(f"  [{\"PASS\" if ok else \"FAIL\"}] POST /api/reports (image)")
    except Exception as e:
        results.append(("POST /api/reports (image)", False, str(e)))
        print(f"  [FAIL] POST /api/reports (image): {e}")

finally:
    proc.terminate()
    proc.wait()
    os.chdir(orig_dir)

print()
print("=" * 60)
print("VERIFICATION RESULTS")
print("=" * 60)
for name, ok, body in results:
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}")
    if isinstance(body, str):
        print(f"    Response: {body[:200]}")
    else:
        print(f"    Response: {json.dumps(body)[:200]}")

print("\nDone.")