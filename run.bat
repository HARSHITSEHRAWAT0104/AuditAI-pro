@echo off
title AuditAI Pro - Enterprise Sales Audit & AI Growth Platform
echo ===================================================================
echo               AuditAI Pro - Sales Audit & Growth Engine
echo ===================================================================
echo [INFO] Starting web server on http://localhost:8000 ...
cd /d "%~dp0"
start http://localhost:8000
.venv\Scripts\python.exe -m uvicorn server:app --host 127.0.0.1 --port 8000
pause
