#!/bin/bash
# Docker entrypoint for Multi-Agent Research System

set -e

echo "Starting Intellecta Multi-Agent Research System..."

# Start Ollama in background
echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Ollama is ready!"
        break
    fi
    sleep 2
done

# Pull model if not present
if ! ollama list | grep -q "llama3.1:8b"; then
    echo "Pulling llama3.1:8b model..."
    ollama pull llama3.1:8b
fi

# Start Streamlit
echo "Starting Streamlit app..."
exec streamlit run app.py --server.port=8501 --server.address=0.0.0.0