# UrbanPulse AI Dashboard - Architecture & Design System

## 🏗️ Application Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Browser                           │
│  ┌────────────────────────────────────────────────────┐    │
│  │         React Frontend (Port 3000)                 │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │         App.tsx (Router)                     │  │    │
│  │  │  ┌────────────────────────────────────────┐  │  │    │
│  │  │  │ Pages                                  │  │  │    │
│  │  │  │ - Overview                             │  │  │    │
│  │  │  │ - Risk Intelligence                    │  │  │    │
│  │  │  │ - Hotspot Predictions                  │  │  │    │
│  │  │  │ - Ward Analytics                       │  │  │    │
│  │  │  │ - Infrastructure Trends                │  │  │    │
│  │  │  │ - Reports                              │  │  │    │
│  │  │  └────────────────────────────────────────┘  │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
                    HTTP/REST API
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                Flask Backend (Port 5000)                    │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Flask REST API (api.py)                    │    │
│  │  ┌────────────────────────────────────────────┐    │    │
│  │  │ Routes:                                    │    │    │
│  │  │ - /api/dashboard/data                     │    │    │
│  │  │ - /api/complaints                         │    │    │
│  │  │ - /api/risk-data                          │    │    │
│  │  │ - /api/hotspots                           │    │    │
│  │  │ - /api/insights                           │    │    │
│  │  │ - /api/trends                             │    │    │
│  │  │ - etc.                                     │    │    │
│  │  └────────────────────────────────────────────┘    │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Data Layer (Python)                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │  CSV Files / Data Processing                      │    │
│  │  - grievances_cleaned.csv                         │    │
│  │  - area_risk_scores.csv                           │    │
│  │  - hotspot_predictions.csv                        │    │
│  │  - area_features.csv                              │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Component Hierarchy

```
App
├── Navbar
│   ├── Logo
│   ├── Status Indicator
│   ├── Notifications
│   └── User Profile
├── Sidebar
│   ├── Navigation Menu
│   │   ├── Overview
│   │   ├── Risk Intelligence
│   │   ├── Hotspot Predictions
│   │   ├── Ward Analytics
│   │   ├── Infrastructure Trends
│   │   └── Reports
│   ├── Settings
│   └── Premium Badge
└── Main Content
    └── Current Page
        ├── HeroSection
        ├── KPI Cards
        │   ├── KPICard
        │   ├── StatCard
        │   └── AnimatedMetrics
        ├── Charts
        │   ├── PremiumChart
        │   │   ├── LineChart
        │   │   ├── AreaChart
        │   │   └── BarChart
        │   └── Tooltip
        ├── Tables
        │   ├── PremiumTable
        │   │   ├── TableHeader
        │   │   ├── TableBody
        │   │   └── ExpandableRow
        │   └── Pagination
        ├── Filters
        │   └── AdvancedFilters
        │       ├── DateRangeFilter
        │       ├── MultiSelectFilter
        │       └── SliderFilter
        ├── AI Insights
        │   └── AIInsightCard
        └── Other Components
            ├── SkeletonLoader
            ├── CommandPalette
            ├── MapTooltip
            └── LoadingAnimation
```

## 🔄 Data Flow

```
User Interaction
    │
    ▼
Component State Update
    │
    ▼
API Service Call (axios)
    │
    ▼
Flask Backend Processing
    │
    ▼
Data Filtering & Aggregation
    │
    ▼
CSV Data Reading
    │
    ▼
JSON Response
    │
    ▼
Component Render with New Data
    │
    ▼
UI Update with Framer Motion
```

## 🎯 Module Organization

### Frontend Modules

**Pages** (`src/pages/`)
- Overview: Dashboard overview with KPIs and trends
- RiskIntelligence: Risk scoring and analysis
- HotspotPredictions: ML-based predictions
- WardAnalytics: Ward-level metrics
- InfrastructureTrends: Degradation and maintenance
- Reports: Report generation and export

**Components** (`src/components/`)
- `layout/`: Navigation and layout (Navbar, Sidebar)
- `KPICard.tsx`: Animated metric cards
- `PremiumChart.tsx`: Interactive charts
- `PremiumTable.tsx`: Data tables
- `HeroSection.tsx`: Overview banner
- `AIInsightCard.tsx`: Insight panels
- `AdvancedFilters.tsx`: Filter system
- `SkeletonLoader.tsx`: Loading states
- `MapTooltip.tsx`: Map interactions
- `CommandPalette.tsx`: Command search
- `StatCard.tsx`: Simple stats

**Services** (`src/services/`)
- `api.ts`: Axios API client with all endpoints

**Utils** (`src/utils/`)
- `cn.ts`: Class name utilities

### Backend Modules

**API** (`src/dashboard/api.py`)
- Flask app initialization
- Route handlers
- Data filtering and aggregation
- CORS configuration

**Data Layer** (`data/processed/`)
- CSV files with processed data
- No modifications to this layer

## 🎨 Design Tokens

### Color Palette

```javascript
const colors = {
  // Primary
  'neon-cyan': '#00d9ff',        // Main brand color
  'neon-blue': '#0099ff',        // Secondary blue
  
  // Accent
  'royal': '#d4af37',            // Gold accent
  'gold': '#ffd700',             // Light gold
  'premium-purple': '#9d4edd',   // Purple accent
  
  // Status
  'emerald-accent': '#00d98e',   // Success/positive
  'rose-accent': '#ff006e',      // Warning/negative
  
  // Backgrounds
  'midnight': '#0a0e27',         // Main dark bg
  'dark-slate': '#1a1f3a',       // Secondary dark
  'graphite': '#2a2f4e',         // Tertiary dark
}
```

### Typography

```javascript
const typography = {
  'font-inter': ['Inter', 'sans-serif'],
  'font-satoshi': ['Satoshi', 'sans-serif'],
  
  sizes: {
    'text-xs': '0.75rem',        // 12px
    'text-sm': '0.875rem',       // 14px
    'text-base': '1rem',         // 16px
    'text-lg': '1.125rem',       // 18px
    'text-xl': '1.25rem',        // 20px
    'text-2xl': '1.5rem',        // 24px
    'text-3xl': '1.875rem',      // 30px
    'text-4xl': '2.25rem',       // 36px
    'text-5xl': '3rem',          // 48px
  },
  
  weights: {
    'font-light': 300,
    'font-normal': 400,
    'font-semibold': 600,
    'font-bold': 700,
  }
}
```

### Spacing

```javascript
const spacing = {
  xs: '0.25rem',   // 4px
  sm: '0.5rem',    // 8px
  base: '1rem',    // 16px
  md: '1.5rem',    // 24px
  lg: '2rem',      // 32px
  xl: '2.5rem',    // 40px
  '2xl': '3rem',   // 48px
}
```

### Shadows

```javascript
const shadows = {
  'shadow-glow': '0 0 30px rgba(0, 217, 255, 0.2)',
  'shadow-premium': '0 20px 60px rgba(0, 0, 0, 0.4)',
  'shadow-inner-glow': 'inset 0 0 20px rgba(212, 175, 55, 0.1)',
}
```

## 🔌 API Integration Points

### API Service Pattern

```typescript
// services/api.ts
export const dashboardAPI = {
  getDashboardData: async (filters?: any) => {
    return api.get<DashboardData>('/dashboard/data', { params: filters })
  },
  getComplaints: async (filters?: any) => {
    return api.get<ComplaintData[]>('/complaints', { params: filters })
  },
  // ... more endpoints
}

// Usage in components
const fetchData = async () => {
  const response = await dashboardAPI.getDashboardData({
    start_date: '2025-01-01',
    end_date: '2025-12-31',
  })
  setData(response.data)
}
```

## ⚡ Performance Optimizations

### Code Splitting
- Lazy load pages with React.lazy()
- Separate vendor bundles
- Optimize chunk size

### Caching Strategy
- API response caching with axios
- Browser cache for static assets
- Service worker for offline support

### Rendering Optimization
- React.memo for expensive components
- useCallback for stable functions
- Virtualization for long lists

### Bundle Size
- Tree shaking with Vite
- Minification and compression
- Image optimization

## 🔐 Security Measures

- CORS enabled for specified origins only
- Input validation on backend
- XSS protection via React's sanitization
- No sensitive data in frontend code
- Environment variables for configuration

## 📱 Responsive Design

### Breakpoints
```javascript
const breakpoints = {
  mobile: '0px',      // 0-640px
  sm: '640px',        // 640px+
  md: '768px',        // 768px+
  lg: '1024px',       // 1024px+
  xl: '1280px',       // 1280px+
  '2xl': '1536px',    // 1536px+
}
```

### Mobile-First Approach
- Design for mobile first
- Enhance for larger screens
- Touch-friendly tap targets
- Simplified navigation on mobile

## 🚀 Deployment Architecture

### Development
```
localhost:3000 (React Dev Server)
      ↓
localhost:5000 (Flask API)
      ↓
Local CSV Files
```

### Production (Docker)
```
Docker Container (Frontend)
      ↓
Docker Container (Backend)
      ↓
Docker Volume (Data)
```

### Cloud Deployment
```
CDN / Vercel (Frontend)
      ↓
Cloud Function / Heroku (API)
      ↓
Cloud Storage / Database
```

---

**This architecture ensures scalability, maintainability, and optimal performance.**
