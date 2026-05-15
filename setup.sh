#!/bin/bash

echo "🚀 UrbanPulse AI Dashboard - Setup Script"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Installing Python dependencies...${NC}"
pip install -r requirements-api.txt

echo -e "${BLUE}Step 2: Setting up frontend...${NC}"
cd frontend
npm install

echo -e "${BLUE}Step 3: Building frontend...${NC}"
npm run build

cd ..

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "To start the dashboard:"
echo "1. Start Flask API: python src/dashboard/api.py"
echo "2. Start React dev server: cd frontend && npm run dev"
echo "3. Open http://localhost:3000 in your browser"
echo ""
echo "For production:"
echo "npm run build in frontend folder creates optimized build"
