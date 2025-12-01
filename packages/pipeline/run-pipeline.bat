@echo off
REM ESIA Pipeline Runner - Auto-activates Python 3.12 Virtual Environment
REM Usage: run-pipeline.bat document.pdf [--steps 1,2,3] [--verbose]

setlocal enabledelayedexpansion

REM Check if PDF file argument provided
if "%~1"=="" (
    echo.
    echo [ERROR] PDF file argument required
    echo.
    echo Usage:
    echo   run-pipeline.bat document.pdf [--steps 1,2,3] [--verbose]
    echo.
    echo Examples:
    echo   run-pipeline.bat data/pdfs/myfile.pdf
    echo   run-pipeline.bat myfile.pdf --steps 1,2,3
    echo   run-pipeline.bat myfile.pdf --verbose
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
set VENV_PATH=%~dp0venv312

if not exist "%VENV_PATH%" (
    echo.
    echo [ERROR] venv312 not found at %VENV_PATH%
    echo.
    echo Please create it first with:
    echo   "M:\Python\Python3_12\python.exe" -m venv venv312
    echo.
    pause
    exit /b 1
)

echo.
echo [INFO] Activating Python 3.12 virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

REM Verify Python version
echo.
echo [INFO] Python Version:
python --version
echo.

REM Build command with all arguments
set ARGS=%*
set PDF_FILE=%~1
set REMAINING_ARGS=%ARGS:*%1 =%

echo [INFO] Running pipeline...
echo Command: python run-esia-pipeline.py "%PDF_FILE%" %REMAINING_ARGS%
echo.

REM Run the pipeline
python run-esia-pipeline.py "%PDF_FILE%" %REMAINING_ARGS%

REM Capture exit code
if %ERRORLEVEL% equ 0 (
    echo.
    echo [SUCCESS] Pipeline completed successfully!
    exit /b 0
) else (
    echo.
    echo [ERROR] Pipeline failed with exit code: %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)
