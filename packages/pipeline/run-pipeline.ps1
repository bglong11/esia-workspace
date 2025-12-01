# ESIA Pipeline Runner - Auto-activates Python 3.12 Virtual Environment
# Usage: .\run-pipeline.ps1 <pdf_file> [--steps 1,2,3] [--verbose]

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$PdfFile,

    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$AdditionalArgs
)

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if venv312 exists
$VenvPath = Join-Path $ScriptDir "venv312"
if (-not (Test-Path $VenvPath)) {
    Write-Host "[ERROR] venv312 not found at $VenvPath" -ForegroundColor Red
    Write-Host "Please create it first with:" -ForegroundColor Yellow
    Write-Host "  `"M:\Python\Python3_12\python.exe`" -m venv venv312" -ForegroundColor Cyan
    exit 1
}

# Activate virtual environment
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
if (-not (Test-Path $ActivateScript)) {
    Write-Host "[ERROR] Activation script not found at $ActivateScript" -ForegroundColor Red
    exit 1
}

Write-Host "[INFO] Activating Python 3.12 virtual environment..." -ForegroundColor Cyan
& $ActivateScript

# Verify Python version
Write-Host ""
Write-Host "[INFO] Python Version:" -ForegroundColor Cyan
python --version
Write-Host ""

# Build the command
$Command = "python run-esia-pipeline.py `"$PdfFile`" $($AdditionalArgs -join ' ')"

Write-Host "[INFO] Running pipeline..." -ForegroundColor Green
Write-Host "Command: $Command" -ForegroundColor Gray
Write-Host ""

# Run the pipeline
Invoke-Expression $Command

# Capture exit code
$ExitCode = $LASTEXITCODE

if ($ExitCode -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] Pipeline completed successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[ERROR] Pipeline failed with exit code: $ExitCode" -ForegroundColor Red
}

exit $ExitCode
