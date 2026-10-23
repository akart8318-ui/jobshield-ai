@echo off
echo ====================================================
echo Starting JobShield AI Backend (FastAPI Server)...
echo ====================================================
cd /d "%~dp0backend"
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
pause
