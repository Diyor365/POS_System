@echo off
REM Simple launcher for POS_System on Windows. Double-click to run.
cd /d "%~dp0"
echo Activating virtual environment if present...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)
python run.py
pause
