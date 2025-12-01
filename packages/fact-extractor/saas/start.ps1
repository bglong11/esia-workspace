# ESIA Fact Extractor SaaS Startup Script (Windows)

Write-Host "========================================"
Write-Host "ESIA Fact Extractor SaaS"
Write-Host "========================================"
Write-Host ""

# Check if Ollama is running
Write-Host "Checking Ollama service..."
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -ErrorAction Stop
    Write-Host "✓ Ollama is running"
} catch {
    Write-Host "⚠️  Ollama is not running!" -ForegroundColor Yellow
    Write-Host "Please start Ollama manually or run: ollama serve"
    $start = Read-Host "Start Ollama now? (y/n)"
    if ($start -eq "y") {
        Write-Host "Starting Ollama in background..."
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 3
    } else {
        exit 1
    }
}

# Check if model exists
Write-Host "Checking for Qwen2.5:7B-Instruct model..."
$models = ollama list
if ($models -notmatch "qwen2.5:7b-instruct") {
    Write-Host "⚠️  Model not found!" -ForegroundColor Yellow
    Write-Host "Pulling model (this may take a while)..."
    ollama pull qwen2.5:7b-instruct
}

# Check Python dependencies
Write-Host "Checking Python dependencies..."
try {
    python -c "import fastapi" 2>$null
    Write-Host "✓ Dependencies installed"
} catch {
    Write-Host "Installing dependencies..."
    pip install -r backend\requirements.txt
}

# Start server
Write-Host ""
Write-Host "Starting FastAPI server..."
Write-Host "Application will be available at: http://localhost:8000"
Write-Host ""
Write-Host "Press Ctrl+C to stop"
Write-Host ""

Set-Location backend
python main.py
