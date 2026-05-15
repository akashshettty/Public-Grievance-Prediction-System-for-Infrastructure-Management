"""
Architecture Documentation
UrbanPulse Project Structure
"""

# Project Directory Structure

```
urbanpluse2/
│
├── backend/                          # Backend API (Flask)
│   ├── api/                         # API layer
│   │   ├── routes/                  # Route blueprints
│   │   │   ├── health_routes.py
│   │   │   ├── dashboard_routes.py
│   │   │   ├── complaint_routes.py
│   │   │   ├── ai_routes.py
│   │   │   └── __init__.py
│   │   ├── schemas/                 # Request/response schemas
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── services/                    # Business logic layer
│   │   ├── data_service.py         # Data access service
│   │   ├── dashboard_service.py    # Dashboard metrics
│   │   ├── complaint_service.py    # Complaint management
│   │   ├── ai_service.py           # AI orchestration
│   │   └── __init__.py
│   ├── config/                      # Configuration
│   │   ├── settings.py             # Environment configs
│   │   └── __init__.py
│   ├── utils/                       # Utility functions
│   │   ├── decorators.py
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   └── __init__.py
│   ├── middleware/                  # Middleware layer
│   │   └── __init__.py
│   └── __init__.py
│
├── ml_modules/                      # Machine Learning Modules
│   ├── nlp/                         # NLP Intelligence
│   │   ├── classifier.py
│   │   └── __init__.py
│   ├── fraud_detection/             # Fraud Detection
│   │   ├── detector.py
│   │   └── __init__.py
│   ├── forecasting/                 # Failure Prediction
│   │   ├── predictor.py
│   │   └── __init__.py
│   ├── escalation/                  # Escalation Prediction
│   │   ├── predictor.py
│   │   └── __init__.py
│   ├── optimization/                # Resource Optimization
│   │   ├── engine.py
│   │   └── __init__.py
│   ├── data_ingestion/              # Data Ingestion Layer
│   │   ├── pipeline.py
│   │   └── __init__.py
│   └── __init__.py
│
├── shared/                          # Shared utilities
│   ├── models/                      # Shared data models
│   │   ├── models.py
│   │   └── __init__.py
│   ├── utils/                       # Shared utilities
│   │   ├── __init__.py
│   └── constants/                   # Constants and enums
│       ├── constants.py
│       └── __init__.py
│
├── frontend/                        # React/TypeScript Frontend
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
│
├── data/                            # Data directory
│   ├── raw/                         # Raw data
│   ├── processed/                   # Processed data
│   │   ├── grievances_cleaned.csv
│   │   ├── area_risk_scores.csv
│   │   ├── hotspot_predictions.csv
│   │   └── area_features.csv
│   └── aligned/
│
├── tests/                           # Test suites
│   ├── unit/
│   │   ├── backend/
│   │   └── ml_modules/
│   ├── integration/
│   └── __init__.py
│
├── docker/                          # Docker files
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── docs/                            # Documentation
│   ├── api/                         # API documentation
│   │   └── endpoints.md
│   ├── architecture/                # Architecture docs
│   │   └── structure.md
│   └── deployment/                  # Deployment guides
│       └── deploy.md
│
├── wsgi.py                          # WSGI entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # Project README
└── .env                             # Environment variables
```

## Architecture Layers

### 1. **Frontend Layer** (React/TypeScript)
- UI Components
- Pages & Views
- API Services
- State Management

### 2. **API Layer** (Flask)
- REST Endpoints
- Request Routing
- Response Formatting
- CORS Handling

### 3. **Service Layer**
- Business Logic
- Data Aggregation
- AI Orchestration
- Data Caching

### 4. **ML Module Layer**
- NLP Intelligence
- Fraud Detection
- Failure Prediction
- Escalation Prediction
- Resource Optimization
- Data Ingestion

### 5. **Data Layer**
- CSV File Storage
- Data Loading
- Caching
- Filtering

## API Routes Structure

### Health Routes (`/api/health`)
- `GET /api/health` - System health check
- `GET /api/health/ready` - Readiness probe
- `GET /api/health/live` - Liveness probe

### Dashboard Routes (`/api/dashboard`)
- `GET /api/dashboard/data` - KPI metrics
- `GET /api/dashboard/trends` - Trend analysis
- `GET /api/dashboard/summary` - Executive summary

### Complaint Routes (`/api/complaints`)
- `GET /api/complaints` - List complaints
- `GET /api/complaints/<id>` - Get complaint detail
- `GET /api/complaints/statistics` - Complaint statistics

### AI Routes (`/api/ai`)
- `GET /api/ai/complaint-analysis` - NLP analysis
- `GET /api/ai/fraud-detection` - Fraud detection
- `GET /api/ai/escalation-risks` - Escalation prediction
- `GET /api/ai/infrastructure-health` - Health scoring
- `GET /api/ai/failure-prediction` - Failure prediction
- `GET /api/ai/resource-optimization` - Resource optimization
- `GET /api/ai/data-ingestion` - Ingestion status

## Configuration Management

The `backend/config/settings.py` file handles environment-specific configurations:
- **DevelopmentConfig**: Debug enabled, verbose logging
- **ProductionConfig**: Debug disabled, minimal logging
- **TestingConfig**: Testing mode configuration

Select config via `FLASK_ENV` environment variable.

## Service Layer Responsibilities

### DataService
- Loads CSV files
- Caches data in memory
- Provides data access methods

### DashboardService
- Aggregates KPI metrics
- Calculates trends
- Generates summaries

### ComplaintService
- Manages complaint data
- Provides filtering and pagination
- Calculates statistics

### AIService
- Orchestrates ML modules
- Aggregates AI outputs
- Provides unified interface

## Key Features

✅ Modular Architecture
✅ Separation of Concerns
✅ Scalable Structure
✅ Configuration Management
✅ Error Handling
✅ Logging
✅ Testing Support
✅ Documentation

## Next Steps (Phase 2)

1. Refactor existing API code to use new structure
2. Implement full AI module integration
3. Add authentication & authorization
4. Create comprehensive test suite
5. Add database layer (if needed)
6. Deploy with Docker
7. Add API documentation (Swagger)
