# activate312.ps1
# Quick activation script for Python 3.12 venv312 environment
# Usage: .\activate312.ps1

Write-Host 'Activating Python 3.12 venv312 environment...' -ForegroundColor Cyan

# Get the script's directory (workspace root)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Path to venv activation script
$venvActivate = Join-Path $scriptDir 'packages\pipeline\venv312\Scripts\Activate.ps1'

# Check if venv exists
if (Test-Path $venvActivate) {
    # Activate the virtual environment
    & $venvActivate

    Write-Host ''
    Write-Host 'Python 3.12 venv312 activated successfully!' -ForegroundColor Green
    Write-Host ''

    # Display Python version
    Write-Host 'Python version:' -ForegroundColor Yellow
    python --version

    Write-Host ''
    Write-Host 'Virtual environment location:' -ForegroundColor Yellow
    $venvPath = Join-Path $scriptDir 'packages\pipeline\venv312'
    Write-Host "  $venvPath" -ForegroundColor White

    Write-Host ''
    Write-Host 'To deactivate, run: deactivate' -ForegroundColor Cyan
} else {
    Write-Host ''
    Write-Host 'Error: venv312 not found!' -ForegroundColor Red
    Write-Host "  Expected location: $venvActivate" -ForegroundColor Yellow
    Write-Host ''
    Write-Host 'Please ensure venv312 is properly installed' -ForegroundColor Yellow
    exit 1
}
