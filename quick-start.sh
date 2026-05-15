#!/bin/bash
# Quick Start Script for UrbanPulse AI Dashboard

set -e

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   UrbanPulse AI - Premium Smart City Dashboard          ║"
echo "║   Quick Start Setup                                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check Node
echo "✓ Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "✗ Node.js not found. Please install Node.js 16+"
    exit 1
fi

echo ""
echo "📦 Installing dependencies..."
echo ""

# Install Python dependencies
echo "Installing Python packages..."
pip install -r requirements-api.txt -q

# Install frontend
echo "Installing Node packages..."
cd frontend
npm install -q
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the dashboard:"
echo ""
echo "   Terminal 1 (Flask API):"
echo "   $ python src/dashboard/api.py"
echo ""
echo "   Terminal 2 (React Frontend):"
echo "   $ cd frontend && npm run dev"
echo ""
echo "   Then open: http://localhost:3000"
echo ""
echo "📚 Documentation: see DASHBOARD_REDESIGN_GUIDE.md"
echo "📖 Frontend README: frontend/README.md"
echo ""
