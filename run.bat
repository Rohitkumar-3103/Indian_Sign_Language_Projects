@echo off
setlocal EnableDelayedExpansion
title "Indian Sign Language (ISL) Recognition and Translation System"

REM Detect Python command
set "PY_CMD="
py -3.12 --version >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PY_CMD=py -3.12"
    goto :FOUND_PY
)

py --version >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PY_CMD=py"
    goto :FOUND_PY
)

python --version >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PY_CMD=python"
    goto :FOUND_PY
)

echo [ERROR] Python was not found in your system PATH!
echo Please install Python 3.10+ from python.org or Microsoft Store.
pause
exit /b 1

:FOUND_PY

REM Handle command-line arguments directly
if /i "%~1"=="app" goto :LAUNCH_APP
if /i "%~1"=="web" goto :LAUNCH_APP
if /i "%~1"=="pipeline" goto :RUN_PIPELINE
if /i "%~1"=="train" goto :TRAIN_MODEL
if /i "%~1"=="extract" goto :EXTRACT_IMAGES
if /i "%~1"=="dict" goto :BUILD_DICT
if /i "%~1"=="papers" goto :PAPERS
if /i "%~1"=="collect" goto :COLLECTOR
if /i "%~1"=="render" goto :RENDER_LANDMARKS
if /i "%~1"=="verify" goto :VERIFY
if /i "%~1"=="install" goto :INSTALL_REQS
if /i "%~1"=="thesis" goto :COMPILE_THESIS

:MENU
cls
echo ==============================================================================
echo    INDIAN SIGN LANGUAGE (ISL) RECOGNITION AND TRANSLATION PLATFORM
echo ==============================================================================
echo    Python Interpreter: !PY_CMD!
echo.
echo   [1] Launch Main ISL Web Application (Flask Server and Live Camera) [Default]
echo   [2] Run Full End-to-End Processing Pipeline (Extract + Train + Verify)
echo   [3] Retrain ISL Machine Learning Classifier (Random Forest 85.2%%)
echo   [4] Process Uploaded Gesture Images -^> Extract 156-D Landmarks
echo   [5] Compile Master ISL Dictionary and Video Demonstration Mappings
echo   [6] Extract Academic Research Paper Assets (18 Papers / 189 Figures)
echo   [7] Launch Interactive Webcam Dataset Collector (Live Recorder)
echo   [8] Render Publication-Grade 3D Skeletal Landmark Keypoint Visualizers
echo   [9] Verify Project Health, Datasets, and Asset Integrity
echo   [I] Install / Update Python Dependencies (requirements.txt)
echo   [T] Recompile LaTeX Thesis Documentation (main.pdf)
echo   [0] Exit
echo ==============================================================================
set "CHOICE=1"
set /p "CHOICE=Enter selection [1-9, I, T, 0] (Press ENTER for [1]): "

if "%CHOICE%"=="1" goto :LAUNCH_APP
if "%CHOICE%"=="2" goto :RUN_PIPELINE
if "%CHOICE%"=="3" goto :TRAIN_MODEL
if "%CHOICE%"=="4" goto :EXTRACT_IMAGES
if "%CHOICE%"=="5" goto :BUILD_DICT
if "%CHOICE%"=="6" goto :PAPERS
if "%CHOICE%"=="7" goto :COLLECTOR
if "%CHOICE%"=="8" goto :RENDER_LANDMARKS
if "%CHOICE%"=="9" goto :VERIFY
if /i "%CHOICE%"=="I" goto :INSTALL_REQS
if /i "%CHOICE%"=="T" goto :COMPILE_THESIS
if "%CHOICE%"=="0" goto :EXIT

echo.
echo [!] Invalid selection, defaulting to option [1].
echo.
timeout /t 2 >nul
goto :LAUNCH_APP

:LAUNCH_APP
cls
echo ==============================================================================
echo    Starting Indian Sign Language (ISL) Recognition Web Application
echo ==============================================================================
echo  - Live Detection Studio (Camera and Dual-Color Skeleton HUD)
echo  - Bidirectional Video Demonstration Player (203 HD Sign Videos)
echo  - Voice-to-Sign Real-Time Transcription
echo  - YouTube-to-Sign Deepgram Nova-2 Integration
echo  - Interactive 204-Sign Dictionary and Split-Screen Camera Challenger
echo.
echo  Access Web App at: http://127.0.0.1:5000
echo  Press Ctrl+C to terminate the web server.
echo ==============================================================================
echo.
!PY_CMD! app.py
goto :AFTER_EXEC

:RUN_PIPELINE
cls
echo ==============================================================================
echo    Executing Full End-to-End Processing Pipeline
echo ==============================================================================
!PY_CMD! ml_pipeline/run_pipeline.py full-pipeline
goto :AFTER_EXEC

:TRAIN_MODEL
cls
echo ==============================================================================
echo    Retraining ISL Machine Learning Classifier
echo ==============================================================================
!PY_CMD! ml_pipeline/run_pipeline.py train
goto :AFTER_EXEC

:EXTRACT_IMAGES
cls
echo ==============================================================================
echo    Extracting 156-D Landmark Features from Uploaded Sign Images
echo ==============================================================================
!PY_CMD! ml_pipeline/run_pipeline.py extract-uploaded
goto :AFTER_EXEC

:BUILD_DICT
cls
echo ==============================================================================
echo    Compiling Master ISL Dictionary and Synchronizing Video Mappings
echo ==============================================================================
!PY_CMD! ml_pipeline/run_pipeline.py build-dict
goto :AFTER_EXEC

:PAPERS
cls
echo ==============================================================================
echo    Extracting Academic Research Paper Figures and Updating Catalog
echo ==============================================================================
!PY_CMD! ml_pipeline/extract_research_paper_assets.py
goto :AFTER_EXEC

:COLLECTOR
cls
echo ==============================================================================
echo    Launching Interactive Webcam Dataset Collector
echo ==============================================================================
!PY_CMD! ml_pipeline/dataset_collector.py
goto :AFTER_EXEC

:RENDER_LANDMARKS
cls
echo ==============================================================================
echo    Rendering Publication-Grade 3D MediaPipe Landmark Visualizations
echo ==============================================================================
!PY_CMD! ml_pipeline/run_pipeline.py render-landmarks
goto :AFTER_EXEC

:VERIFY
cls
echo ==============================================================================
echo    Running Project Health, Models, and Asset Verification
echo ==============================================================================
!PY_CMD! ml_pipeline/run_pipeline.py verify
goto :AFTER_EXEC

:INSTALL_REQS
cls
echo ==============================================================================
echo    Installing / Updating Python Dependencies from requirements.txt
echo ==============================================================================
!PY_CMD! -m pip install -r requirements.txt
goto :AFTER_EXEC

:COMPILE_THESIS
cls
echo ==============================================================================
echo    Recompiling LaTeX Thesis Documentation
echo ==============================================================================
if not exist thesis_template_0.1 (
    echo [INFO] LaTeX thesis source folder is not present.
    echo Master thesis document is preserved at root: main.pdf
    goto :AFTER_EXEC
)
where pdflatex >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [ERROR] pdflatex not found in PATH! Make sure MiKTeX or TeXLive is installed.
    goto :AFTER_EXEC
)
cd thesis_template_0.1
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
copy /y main.pdf ..\main.pdf >nul
cd ..
echo.
echo [OK] Thesis compilation finished! Updated main.pdf in root directory.
goto :AFTER_EXEC

:AFTER_EXEC
if not "%~1"=="" (
    exit /b 0
)
echo.
echo ==============================================================================
echo Execution complete.
pause
goto :MENU

:EXIT
echo Goodbye!
exit /b 0
