# AuditAI Pro - PowerShell Startup Script
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "          AuditAI Pro - Sales Audit & Growth Engine                " -ForegroundColor White
Write-Host "===================================================================" -ForegroundColor Cyan
Write-Host "[INFO] Opening browser and launching application..." -ForegroundColor Green

Set-Location $PSScriptRoot
Start-Process "http://localhost:8000"
& "$PSScriptRoot\.venv\Scripts\python.exe" -m uvicorn server:app --host 127.0.0.1 --port 8000
