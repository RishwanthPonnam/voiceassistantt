@echo off
REM Git sync batch script

cd /d C:\Users\Rishwanth\Desktop\voiceassistant

echo.
echo ==============================
echo  Git Sync Process Starting
echo ==============================
echo.

echo [Step 1] Pulling from GitHub...
git pull origin main
if errorlevel 1 (
    echo WARNING: Pull returned error code
)

echo.
echo [Step 2] Adding changes...
git add backend/utils/helper.py backend/utils/app_finder.py sync.ps1
if errorlevel 1 (
    echo ERROR: Adding files failed
    exit /b 1
)

echo.
echo [Step 3] Committing...
git commit -m "feat: Add WhatsApp Web fallback and advanced app finder - Synced from local changes"
if errorlevel 1 (
    echo WARNING: Commit may have nothing to commit
)

echo.
echo [Step 4] Pushing to GitHub...
git push origin main
if errorlevel 1 (
    echo ERROR: Push failed
    exit /b 1
)

echo.
echo [Step 5] Final status...
git status

echo.
echo ==============================
echo  Success! Changes synced!
echo ==============================
pause
