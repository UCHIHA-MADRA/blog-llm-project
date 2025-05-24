#!/bin/bash

echo "🚀 Starting Blog LLM Project..."

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install Ollama first:"
    echo "   Visit: https://ollama.ai"
    exit 1
fi

# Start Ollama service
echo "📦 Starting Ollama service..."
ollama serve &
sleep 5

# Pull the model if not exists
echo "🤖 Checking for Llama 3.2 1B model..."
if ! ollama list | grep -q "llama3.2:1b"; then
    echo "📥 Downloading Llama 3.2 1B model..."
    ollama pull llama3.2:1b
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Start the API server
echo "🌐 Starting API server..."
cd api
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# Wait for API to start
sleep 5

# Start simple HTTP server for frontend
echo "🎨 Starting frontend server..."
cd ../frontend
python -m http.server 8080 &

echo "✅ All services started!"
echo ""
echo "🌐 Frontend: http://localhost:8080"
echo "🔧 API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
wait

# Open browser to demo page
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8080/demo.html
elif command -v open > /dev/null; then
    open http://localhost:8080/demo.html
fi

echo "✅ Blog LLM Project is running!"
echo "API: http://localhost:8000"
echo "Demo: http://localhost:8080/demo.html"
echo "API Docs: http://localhost:8000/docs"

# Keep script running
wait