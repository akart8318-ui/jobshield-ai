@echo off
echo =========================================================================
echo JobShield AI - Instant Public Live Tunnel (for Hackathon Judges)
echo =========================================================================
echo.
echo Make sure start_backend.bat is running in another window!
echo Generating instant public HTTPS URL...
echo.
npx localtunnel --port 8000
pause
