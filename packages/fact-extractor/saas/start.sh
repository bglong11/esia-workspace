#!/bin/bash

echo "========================================"
echo "ESIA Fact Extractor SaaS"
echo "========================================"
echo ""

# Check if Ollama is running
echo "Checking Ollama service..."
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "⚠️  Ollama is not running!"
    echo "Please start Ollama with: ollama serve"
    echo ""
    read -p "Start Ollama now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Starting Ollama in background..."
        ollama serve &
        sleep 3
    else
        exit 1
    fi
fi

# Check if model exists
echo "Checking for Qwen2.5:7B-Instruct model..."
if ! ollama list | grep -q "qwen2.5:7b-instruct"; then
    echo "⚠️  Model not found!"
    echo "Pulling model (this may take a while)..."
    ollama pull qwen2.5:7b-instruct
fi

# Check Python dependencies
echo "Checking Python dependencies..."
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r backend/requirements.txt
fi

# Start server
echo ""
echo "Starting FastAPI server..."
echo "Application will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

cd backend
python3 main.py
