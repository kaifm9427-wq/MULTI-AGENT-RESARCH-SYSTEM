#!/bin/bash

# ResearchMind Startup Script
# Runs the multi-agent AI research system

set -e  # Exit on error

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  ResearchMind Startup                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Python detected: $(python3 --version)"

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found"
    echo "💡 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check dependencies
if ! python3 -c "import uvicorn, fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -q -r backend/requirements.txt
fi

# Check API keys
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env not found"
    echo "💡 Please copy config/.env.example to backend/.env and add your API keys"
    exit 1
fi

# Check if required keys are set
if ! grep -q "GEMINI_API_KEY" backend/.env || ! grep -q "TAVILY_API_KEY" backend/.env; then
    echo "⚠️  Warning: API keys might not be configured in backend/.env"
fi

echo ""
echo "🚀 Starting ResearchMind server..."
echo ""
echo "📡 Server Details:"
echo "   • URL: http://localhost:8000"
echo "   • Backend: FastAPI with Uvicorn"
echo "   • Frontend: Premium dark theme"
echo ""
echo "💡 Next steps:"
echo "   1. Open http://localhost:8000 in your browser"
echo "   2. Enter a research topic"
echo "   3. Click 'Run Research Pipeline'"
echo ""
echo "🛑 To stop: Press Ctrl+C"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# Run the server
python3 start.py
