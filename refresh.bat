@echo off
REM Refresh the portfolio from the private CV workbook. Extra options: --preview, --push
cd /d "%~dp0"
where py >nul 2>nul && (py -3 tools\refresh.py %*) || (python tools\refresh.py %*)
pause
