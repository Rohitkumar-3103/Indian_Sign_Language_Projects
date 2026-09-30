@echo off
title Indian Sign Language - Standalone OpenCV Detector
cd /d "%~dp0"
echo ============================================================
echo  Starting Standalone ISL Detector (OpenCV + MediaPipe)
echo ============================================================
echo.

:: Try Python 3.12, then Python 3.10, then default python
py -3.12 isl_detection.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying fallback Python launcher...
    py -3.10 isl_detection.py
)
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Trying default python...
    python isl_detection.py
)

pause
