<#
.SYNOPSIS
    Indian Sign Language (ISL) Interactive Startup & Processing Runner
.DESCRIPTION
    Provides an interactive menu and direct CLI options to launch the web application,
    run the machine learning pipeline, retrain models, extract features, and compile documentation.
.EXAMPLE
    .\run.ps1
    .\run.ps1 app
    .\run.ps1 train
    .\run.ps1 pipeline
    .\run.ps1 verify
#>

[CmdletBinding()]
param (
    [Parameter(Position = 0, Mandatory = $false)]
    [ValidateSet("app", "web", "pipeline", "train", "extract", "dict", "papers", "collect", "render", "verify", "install", "thesis")]
    [string]$Action
)

$OutputEncoding = [System.Text.Encoding]::UTF8

# Locate Python
$PyExe = "python"
$PyArgs = @()

if (Get-Command "py" -ErrorAction SilentlyContinue) {
    $ver = & py -3.12 --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $PyExe = "py"
        $PyArgs = @("-3.12")
    } else {
        $PyExe = "py"
    }
} elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    $PyExe = "python"
} else {
    Write-Host "[ERROR] Python was not found in your system PATH!" -ForegroundColor Red
    exit 1
}

$PyDisplay = "$PyExe $($PyArgs -join ' ')".Trim()

function Show-Header {
    Clear-Host
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host "   🤟 INDIAN SIGN LANGUAGE (ISL) RECOGNITION & TRANSLATION PLATFORM" -ForegroundColor Green
    Write-Host "==============================================================================" -ForegroundColor Cyan
    Write-Host "   Python Interpreter: $PyDisplay" -ForegroundColor Gray
    Write-Host ""
}

function Invoke-Action([string]$act) {
    switch ($act) {
        "app" {
            Show-Header
            Write-Host "Starting Flask Web Application..." -ForegroundColor Yellow
            Write-Host "Web URL: http://127.0.0.1:5000" -ForegroundColor Green
            Write-Host "Press Ctrl+C to stop the server." -ForegroundColor Gray
            Write-Host "------------------------------------------------------------------------------" -ForegroundColor Cyan
            & $PyExe @PyArgs app.py
        }
        "web" {
            Invoke-Action "app"
        }
        "pipeline" {
            Show-Header
            Write-Host "Executing Full ML Processing Pipeline..." -ForegroundColor Yellow
            & $PyExe @PyArgs ml_pipeline/run_pipeline.py full-pipeline
        }
        "train" {
            Show-Header
            Write-Host "Retraining Machine Learning Classifier..." -ForegroundColor Yellow
            & $PyExe @PyArgs ml_pipeline/run_pipeline.py train
        }
        "extract" {
            Show-Header
            Write-Host "Extracting Landmark Features from Uploaded Sign Images..." -ForegroundColor Yellow
            & $PyExe @PyArgs ml_pipeline/run_pipeline.py extract-uploaded
        }
        "dict" {
            Show-Header
            Write-Host "Compiling Master ISL Sign Dictionary..." -ForegroundColor Yellow
            & $PyExe @PyArgs ml_pipeline/run_pipeline.py build-dict
        }
        "papers" {
            Show-Header
            Write-Host "Extracting Academic Research Paper Assets..." -ForegroundColor Yellow
            & $PyExe @PyArgs ml_pipeline/extract_research_paper_assets.py
        }
        "collect" {
            Show-Header
            Write-Host "Launching Interactive Webcam Dataset Collector..." -ForegroundColor Yellow
            & $PyExe @PyArgs ml_pipeline/dataset_collector.py
        }
        "render" {
            Show-Header
            Write-Host "Rendering Publication-Grade 3D Skeletal Landmark Diagrams..." -ForegroundColor Yellow
            & $PyExe @PyArgs ml_pipeline/run_pipeline.py render-landmarks
        }
        "verify" {
            Show-Header
            Write-Host "Verifying Project Datasets, Models, and Assets..." -ForegroundColor Yellow
            & $PyExe @PyArgs ml_pipeline/run_pipeline.py verify
        }
        "install" {
            Show-Header
            Write-Host "Installing / Updating Dependencies..." -ForegroundColor Yellow
            & $PyExe @PyArgs -m pip install -r requirements.txt
        }
        "thesis" {
            Show-Header
            Write-Host "Recompiling LaTeX Thesis Documentation..." -ForegroundColor Yellow
            if (-not (Test-Path "thesis_template_0.1")) {
                Write-Host "[INFO] LaTeX thesis source folder is not present. Master document preserved at main.pdf" -ForegroundColor Green
                return
            }
            if (-not (Get-Command "pdflatex" -ErrorAction SilentlyContinue)) {
                Write-Host "[ERROR] pdflatex not found in PATH! Ensure MiKTeX or TeXLive is installed." -ForegroundColor Red
                return
            }
            Push-Location thesis_template_0.1
            try {
                pdflatex -interaction=nonstopmode main.tex
                pdflatex -interaction=nonstopmode main.tex
                Copy-Item -Path "main.pdf" -Destination "..\main.pdf" -Force
                Write-Host "`n[OK] Thesis compiled successfully into main.pdf!" -ForegroundColor Green
            } finally {
                Pop-Location
            }
        }
    }
}

if ($Action) {
    Invoke-Action $Action
    exit 0
}

# Interactive Menu Loop
while ($true) {
    Show-Header
    Write-Host "  [1] Launch Main ISL Web Application (Flask + Live Camera) [Default]" -ForegroundColor White
    Write-Host "  [2] Run Full End-to-End Processing Pipeline (Extract + Train + Verify)" -ForegroundColor White
    Write-Host "  [3] Retrain ISL Machine Learning Classifier (Random Forest 85.2%)" -ForegroundColor White
    Write-Host "  [4] Process Uploaded Gesture Images -> Extract 156-D Landmarks" -ForegroundColor White
    Write-Host "  [5] Compile Master ISL Dictionary & Video Demonstration Mappings" -ForegroundColor White
    Write-Host "  [6] Extract Academic Research Paper Assets (18 Papers / 189 Figures)" -ForegroundColor White
    Write-Host "  [7] Launch Interactive Webcam Dataset Collector (Live Recorder)" -ForegroundColor White
    Write-Host "  [8] Render Publication-Grade 3D Skeletal Landmark Keypoint Visualizers" -ForegroundColor White
    Write-Host "  [9] Verify Project Health, Datasets, and Asset Integrity" -ForegroundColor White
    Write-Host "  [I] Install / Update Python Dependencies (requirements.txt)" -ForegroundColor White
    Write-Host "  [T] Recompile LaTeX Thesis Documentation (main.pdf)" -ForegroundColor White
    Write-Host "  [0] Exit" -ForegroundColor Red
    Write-Host "==============================================================================" -ForegroundColor Cyan

    $choice = Read-Host "Enter selection [1-9, I, T, 0] (Press Enter for [1])"
    if ([string]::IsNullOrWhiteSpace($choice)) { $choice = "1" }

    switch ($choice.ToUpper()) {
        "1" { Invoke-Action "app" }
        "2" { Invoke-Action "pipeline" }
        "3" { Invoke-Action "train" }
        "4" { Invoke-Action "extract" }
        "5" { Invoke-Action "dict" }
        "6" { Invoke-Action "papers" }
        "7" { Invoke-Action "collect" }
        "8" { Invoke-Action "render" }
        "9" { Invoke-Action "verify" }
        "I" { Invoke-Action "install" }
        "T" { Invoke-Action "thesis" }
        "0" { Write-Host "`nExiting. Goodbye!" -ForegroundColor Green; exit 0 }
        default {
            Write-Host "`nInvalid selection. Press any key to continue..." -ForegroundColor Yellow
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            continue
        }
    }

    Write-Host "`nExecution completed. Press any key to return to menu..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
