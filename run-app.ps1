# ESIA Workspace - Run Frontend & Backend Servers
# Run from root folder: .\run-app.ps1

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  ESIA Workspace - Starting Servers" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration - use Get-Location for reliability
$rootPath = Get-Location
$appPath = Join-Path $rootPath "packages" "app"
$backendPort = 5000
$frontendPort = 3000

Write-Host "[*] Root path: $rootPath" -ForegroundColor Gray
Write-Host "[*] App path: $appPath" -ForegroundColor Gray
Write-Host ""

# Verify paths exist
if (-not (Test-Path $appPath)) {
    Write-Host "[ERROR] packages/app directory not found at: $appPath" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] App directory verified" -ForegroundColor Green
Write-Host ""

# Check if node processes are already running
Write-Host "[*] Checking for existing Node processes..." -ForegroundColor Yellow
$existingProcesses = @(Get-Process node -ErrorAction SilentlyContinue)

if ($existingProcesses.Count -gt 0) {
    Write-Host "[!] Found $($existingProcesses.Count) existing Node process(es)" -ForegroundColor Yellow
    $response = Read-Host "Kill them? (y/n)"
    if ($response -eq 'y') {
        Write-Host "[*] Killing existing Node processes..." -ForegroundColor Yellow
        Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
        Start-Sleep -Seconds 2
        Write-Host "[OK] Old processes killed" -ForegroundColor Green
    } else {
        Write-Host "[*] Skipping cleanup" -ForegroundColor Yellow
    }
}

Write-Host ""

# Start Backend Server in new window
Write-Host "[*] Starting Backend Server (port $backendPort)..." -ForegroundColor Cyan
$backendCmd = "cd `"$appPath`"; node server.js"
Start-Process powershell.exe -ArgumentList "-NoExit -Command $backendCmd"

Start-Sleep -Seconds 3
Write-Host "[OK] Backend server started in new window" -ForegroundColor Green
Write-Host ""

# Start Frontend Server in new window
Write-Host "[*] Starting Frontend Server (port $frontendPort)..." -ForegroundColor Cyan
$frontendCmd = "cd `"$appPath`"; npx vite"
Start-Process powershell.exe -ArgumentList "-NoExit -Command $frontendCmd"

Start-Sleep -Seconds 2
Write-Host "[OK] Frontend server started in new window" -ForegroundColor Green
Write-Host ""

Write-Host "========================================================" -ForegroundColor Green
Write-Host "  SERVERS STARTED" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access the app:" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:$frontendPort" -ForegroundColor Cyan
Write-Host "  Backend:  http://localhost:$backendPort" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Open http://localhost:$frontendPort in browser" -ForegroundColor Gray
Write-Host "  2. Upload a PDF file" -ForegroundColor Gray
Write-Host "  3. Watch the pipeline execute" -ForegroundColor Gray
Write-Host ""
Write-Host "Tips:" -ForegroundColor Yellow
Write-Host "  - Both server windows will stay open" -ForegroundColor Gray
Write-Host "  - Close windows to stop servers" -ForegroundColor Gray
Write-Host "  - Check server logs for real-time updates" -ForegroundColor Gray
Write-Host ""
