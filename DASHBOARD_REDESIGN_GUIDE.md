# Complete Setup Guide for UrbanPulse AI Dashboard Redesign

## 📋 Project Overview

Your UrbanPulse AI dashboard has been completely redesigned from a technical Streamlit interface into a premium, enterprise-grade Smart City Intelligence Platform UI built with modern technologies.

### Technology Stack

**Frontend:**
- React 18 with TypeScript
- TailwindCSS for styling
- Framer Motion for animations
- Recharts for data visualization
- Vite as build tool

**Backend:**
- Flask for REST API
- Python for data processing (existing)
- CORS enabled for frontend communication

**Design System:**
- Midnight blue / graphite black backgrounds
- Royal gold and neon cyan accents
- Glassmorphism effects
- Smooth animations and transitions
- Enterprise-grade professional aesthetics

---

## 🚀 Quick Start Guide

### Prerequisites
- Node.js 16+ and npm/yarn
- Python 3.8+
- Git (optional)

### Step 1: Install Backend Dependencies

```bash
# Install Flask API dependencies
pip install -r requirements-api.txt

# Or if you want to keep both Streamlit and API:
pip install flask flask-cors
```

### Step 2: Start the Flask API Server

```bash
# From project root
python src/dashboard/api.py

# Server runs on http://localhost:5000
# API available at http://localhost:5000/api
```

### Step 3: Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Create .env file (already created) pointing to backend
cat .env  # Shows: REACT_APP_API_URL=http://localhost:5000/api
```

### Step 4: Run Development Server

```bash
# From frontend directory
npm run dev
# or
yarn dev

# Dashboard available at http://localhost:3000
```

---

## 📁 Project Structure

```
f:\Urbanpluse\
├── src/
│   ├── dashboard/
│   │   ├── app.py                 # Original Streamlit app
│   │   ├── api.py                 # NEW: Flask REST API
│   │   └── run_dashboard.py        # Streamlit runner
│   ├── data/                       # Data processing (unchanged)
│   ├── features/                   # Feature engineering (unchanged)
│   ├── models/                     # ML models (unchanged)
│   └── visualization/              # Visualization (unchanged)
│
├── frontend/                       # NEW: React dashboard
│   ├── src/
│   │   ├── App.tsx                # Main app component
│   │   ├── main.tsx               # Entry point
│   │   ├── index.css              # Global styles
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Navbar.tsx      # Top navigation
│   │   │   │   └── Sidebar.tsx     # Side menu
│   │   │   ├── KPICard.tsx         # KPI display cards
│   │   │   ├── PremiumTable.tsx    # Data tables
│   │   │   ├── PremiumChart.tsx    # Charts
│   │   │   ├── HeroSection.tsx     # Hero overview
│   │   │   ├── AIInsightCard.tsx   # AI insights
│   │   │   ├── AdvancedFilters.tsx # Filter controls
│   │   │   └── SkeletonLoader.tsx  # Loading state
│   │   ├── pages/
│   │   │   ├── Overview.tsx        # Dashboard overview
│   │   │   ├── RiskIntelligence.tsx# Risk analysis
│   │   │   ├── HotspotPredictions.tsx # Predictions
│   │   │   ├── WardAnalytics.tsx   # Ward metrics
│   │   │   ├── InfrastructureTrends.tsx # Trends
│   │   │   └── Reports.tsx         # Reports & exports
│   │   ├── services/
│   │   │   └── api.ts             # API service layer
│   │   └── utils/
│   │       └── cn.ts              # Utility functions
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env                       # Development config
│   ├── .env.production            # Production config
│   └── index.html
│
├── requirements.txt               # Original Python deps
├── requirements-api.txt           # Flask API deps (NEW)
├── config/                        # Config files
├── data/                          # Data directory
└── outputs/                       # Output directory
```

---

## 🎨 Design Features

### Premium Visual Elements
✅ Glassmorphism cards with blur effects
✅ Gradient overlays (cyan, gold, purple)
✅ Smooth animations on hover and interaction
✅ Dark luxury theme (midnight blue background)
✅ Royal gold and neon cyan accents
✅ Soft shadows and glow effects
✅ Responsive grid layouts
✅ Professional typography (Inter font)

### Key Components

**1. Navigation (Navbar + Sidebar)**
- Compact, premium navigation
- System status indicator
- User profile section
- Notification bell
- Collapsible on mobile

**2. Dashboard Pages**
- **Overview**: KPI cards, AI insights, trend charts
- **Risk Intelligence**: Risk scoring, area assessment
- **Hotspot Predictions**: ML predictions with timelines
- **Ward Analytics**: Area-wise performance metrics
- **Infrastructure Trends**: Degradation analysis
- **Reports**: Report generation and data export

**3. UI Components**
- **KPICard**: Animated metric cards with trends and sparklines
- **PremiumTable**: Sortable tables with expandable rows
- **PremiumChart**: Interactive charts (line, area, bar)
- **AIInsightCard**: AI-generated insights with severity levels
- **HeroSection**: Hero banner with key metrics
- **AdvancedFilters**: Collapsible filter drawer

### Animations
- Smooth page transitions
- Hover effects on interactive elements
- Loading skeleton animations
- Animated metric counters
- Floating background elements

---

## 📊 API Endpoints

The Flask API provides the following endpoints:

```
GET  /api/health                    # Health check
GET  /api/dashboard/data            # KPI metrics
GET  /api/complaints                # Complaint records
GET  /api/risk-data                 # Risk scores
GET  /api/hotspots                  # Hotspot predictions
GET  /api/area-features             # Area features
GET  /api/heatmap                   # Heatmap HTML
GET  /api/insights                  # AI insights
GET  /api/trends                    # Trend data
```

### Request Parameters
```
?start_date=2025-01-01
?end_date=2025-12-31
?issue_types=road,water,drainage
?areas=KR%20Puram,Indiranagar,Whitefield
?status=open
```

### Example API Call
```bash
curl http://localhost:5000/api/dashboard/data \
  ?start_date=2025-01-01 \
  ?end_date=2025-12-31 \
  ?issue_types=road,water
```

---

## 🔧 Configuration

### Frontend Configuration (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_ENV=development
```

### Backend Configuration (api.py)
Flask runs on port 5000 with CORS enabled for localhost:3000

### TailwindCSS Custom Colors
- `midnight`: #0a0e27 (Dark background)
- `dark-slate`: #1a1f3a (Secondary dark)
- `graphite`: #2a2f4e (Tertiary dark)
- `royal`: #d4af37 (Gold accent)
- `gold`: #ffd700 (Lighter gold)
- `neon-cyan`: #00d9ff (Primary cyan)
- `neon-blue`: #0099ff (Blue accent)
- `premium-purple`: #9d4edd (Purple accent)

---

## 🎯 Features

### Dashboard Features
✅ Real-time KPI metrics
✅ AI-driven insights and alerts
✅ Advanced filtering system
✅ Interactive charts and visualizations
✅ Expandable data tables
✅ Risk intelligence analysis
✅ Hotspot predictions with ML
✅ Ward-level performance metrics
✅ Infrastructure health tracking
✅ Trend analysis and forecasting
✅ Report generation
✅ Data export functionality

### User Experience
✅ Non-technical friendly UI
✅ Clear information hierarchy
✅ Visual storytelling
✅ Color-coded severity levels
✅ Smooth animations
✅ Responsive design
✅ Mobile optimized
✅ Loading states with skeletons
✅ Error handling

---

## 🚀 Deployment

### Production Build
```bash
cd frontend
npm run build

# Dist folder contains optimized production build
# Deploy to any static hosting (Vercel, Netlify, etc.)
```

### Docker Deployment (Optional)
```dockerfile
# Create Dockerfile for frontend
FROM node:18-alpine
WORKDIR /app
COPY frontend . 
RUN npm install && npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### Backend Deployment
```bash
# Use gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.dashboard.api:app
```

---

## 📦 Maintenance

### Adding New Pages
1. Create new component in `src/pages/`
2. Add route in `App.tsx`
3. Add navigation item in `Sidebar.tsx`

### Updating API
1. Modify endpoints in `src/dashboard/api.py`
2. Update API service in `frontend/src/services/api.ts`
3. Use new endpoints in components

### Custom Styling
1. Update `tailwind.config.js` for colors/animations
2. Add global styles to `src/index.css`
3. Use Tailwind classes in components

---

## 🐛 Troubleshooting

**Frontend won't connect to API:**
- Check Flask is running on http://localhost:5000
- Verify CORS is enabled in `api.py`
- Check .env file has correct API_URL

**Data not loading:**
- Verify CSV files exist in `data/processed/`
- Check file paths in `api.py`
- Run data preprocessing pipeline first

**Styling issues:**
- Rebuild with `npm run build`
- Clear browser cache
- Check TailwindCSS is compiled

**Performance issues:**
- Check React DevTools for re-renders
- Optimize chart data size
- Use React.memo for heavy components

---

## 📝 Development Commands

```bash
# Frontend
cd frontend
npm install          # Install dependencies
npm run dev         # Start dev server (port 3000)
npm run build       # Build for production
npm run preview     # Preview production build
npm run lint        # Run linter

# Backend
python src/dashboard/api.py  # Start Flask server (port 5000)

# Data Processing
python src/data/run_preprocessing.py
python src/features/run_feature_risk.py
python src/models/run_hotspot_prediction.py
```

---

## 🎓 Learning Resources

### Component Architecture
- Pages: Full page views
- Components: Reusable UI elements
- Services: API communication
- Utils: Helper functions

### State Management
- React hooks (useState, useEffect)
- Could integrate Zustand for global state
- API service for data fetching

### Styling
- TailwindCSS utility classes
- Framer Motion for animations
- CSS custom properties for theming

---

## 📞 Support

For issues or questions:
1. Check logs in browser console
2. Review Flask server output
3. Check .env configuration
4. Verify data files exist

---

## 🎉 Next Steps

1. ✅ Complete React frontend setup
2. ✅ Start Flask API server
3. ✅ Connect frontend to backend
4. ✅ Load existing data
5. Test all pages and features
6. Customize colors/branding
7. Deploy to production

---

**Your UrbanPulse AI dashboard is now a premium, enterprise-grade Smart City Intelligence Platform!**

Enjoy your new modern, beautiful, and functional dashboard! 🚀
