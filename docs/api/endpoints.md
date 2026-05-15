"""
API Endpoints Documentation
UrbanPulse REST API
"""

# API Endpoints Reference

## Base URL
```
http://localhost:5000
```

## Health Check Endpoints

### System Health
```
GET /api/health
```
**Description:** Check overall system health
**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-13T21:36:00",
  "version": "2.0.0"
}
```

### Readiness Probe
```
GET /api/health/ready
```
**Description:** Check if system is ready to serve traffic
**Response:**
```json
{
  "ready": true,
  "timestamp": "2026-05-13T21:36:00"
}
```

### Liveness Probe
```
GET /api/health/live
```
**Description:** Check if system is alive
**Response:**
```json
{
  "alive": true,
  "timestamp": "2026-05-13T21:36:00"
}
```

---

## Dashboard Endpoints

### Get Dashboard Metrics
```
GET /api/dashboard/data
```
**Query Parameters:**
- `start_date` (optional): ISO format date
- `end_date` (optional): ISO format date
- `areas` (optional): Comma-separated area names

**Response:**
```json
{
  "metrics": {
    "total_complaints": 12458,
    "open_complaints": 3247,
    "closed_complaints": 9211,
    "high_risk_areas": 24,
    "predicted_hotspots": 8,
    "infrastructure_health": 78,
    "avg_response_time": 4.2,
    "complaint_growth_percent": 12.5
  },
  "timestamp": "2026-05-13T21:36:00"
}
```

### Get Trends
```
GET /api/dashboard/trends
```
**Query Parameters:**
- `days` (optional, default: 30): Number of days to retrieve

**Response:**
```json
{
  "data": [
    {
      "date": "2026-05-13",
      "complaint_count": 45
    }
  ]
}
```

### Get Summary
```
GET /api/dashboard/summary
```
**Response:**
```json
{
  "summary": {
    "status": "Operational",
    "overall_health": 78,
    "critical_alerts": 3,
    "metrics": { ... }
  }
}
```

---

## Complaint Endpoints

### List Complaints
```
GET /api/complaints
```
**Query Parameters:**
- `status` (optional): open, closed, in_progress, etc.
- `area` (optional): Filter by area/ward
- `issue_type` (optional): Filter by issue type
- `limit` (optional, default: 100): Number of results
- `offset` (optional, default: 0): Pagination offset

**Response:**
```json
{
  "data": [
    {
      "id": "COMP-001",
      "description": "Pothole in main road",
      "area": "Ward 5",
      "issue_type": "Road Infrastructure",
      "status": "open",
      "severity": 0.85,
      "created_at": "2026-05-13T10:00:00"
    }
  ],
  "count": 100,
  "total": 3247,
  "offset": 0,
  "limit": 100
}
```

### Get Complaint Detail
```
GET /api/complaints/{complaint_id}
```
**Response:**
```json
{
  "id": "COMP-001",
  "description": "Pothole in main road",
  "area": "Ward 5",
  "issue_type": "Road Infrastructure",
  "status": "open",
  "severity": 0.85,
  "created_at": "2026-05-13T10:00:00",
  "closed_at": null,
  "reopening_count": 0
}
```

### Get Complaint Statistics
```
GET /api/complaints/statistics
```
**Query Parameters:**
- `group_by` (optional): status, area, or issue_type

**Response:**
```json
{
  "data": [
    {
      "status": "open",
      "count": 3247
    },
    {
      "status": "closed",
      "count": 9211
    }
  ],
  "grouped_by": "status"
}
```

---

## AI Module Endpoints

### Complaint Analysis (NLP)
```
GET /api/ai/complaint-analysis
```
**Query Parameters:**
- `limit` (optional, default: 50): Number of complaints to analyze

**Response:**
```json
{
  "data": [
    {
      "id": "COMP-001",
      "classification": "Road Infrastructure",
      "confidence": 0.95,
      "severity_score": 0.85,
      "sentiment": "neutral"
    }
  ],
  "stats": {
    "total_analyzed": 50,
    "avg_confidence": 0.95,
    "accuracy_rate": 0.95
  }
}
```

### Fraud Detection
```
GET /api/ai/fraud-detection
```
**Response:**
```json
{
  "alerts": [
    {
      "id": "ALERT-001",
      "complaint_id": "COMP-001",
      "fraud_score": 0.82,
      "anomaly_type": "Premature Closure",
      "reason": "High severity complaint closed in 2.3 hours",
      "severity": "high"
    }
  ],
  "stats": {
    "total_analyzed": 1000,
    "flagged_count": 5,
    "fraud_rate": 0.005,
    "precision": 0.87
  }
}
```

### Escalation Risks
```
GET /api/ai/escalation-risks
```
**Response:**
```json
{
  "risks": [
    {
      "complaint_id": "COMP-001",
      "ward": "Ward 5",
      "issue_type": "Road Collapse",
      "risk_level": "critical",
      "escalation_probability": 0.92,
      "days_until_escalation": 2,
      "social_mentions": 247,
      "news_coverage": true
    }
  ],
  "stats": {
    "total_monitored": 5000,
    "critical_count": 3,
    "accuracy": 0.84
  }
}
```

### Infrastructure Health
```
GET /api/ai/infrastructure-health
```
**Query Parameters:**
- `areas` (optional): Comma-separated area names

**Response:**
```json
{
  "health_scores": [
    {
      "area": "Ward 5",
      "overall_score": 78,
      "components": {
        "road_condition": 75,
        "drainage_system": 80,
        "water_supply": 78,
        "utilities": 85,
        "sanitation": 72
      },
      "status": "Good"
    }
  ],
  "stats": {
    "overall_health_score": 78,
    "areas_monitored": 30,
    "critical_areas": 5
  }
}
```

### Failure Prediction
```
GET /api/ai/failure-prediction
```
**Response:**
```json
{
  "predictions": [
    {
      "issue_type": "Road Collapse",
      "area": "Ward 5",
      "predicted_date": "2026-05-20T00:00:00",
      "lead_time_days": 7,
      "confidence": 0.87,
      "severity": "Critical",
      "recommended_action": "Schedule preventive maintenance"
    }
  ],
  "stats": {
    "total_predictions": 8,
    "average_lead_time": 10,
    "avg_confidence": 0.85
  }
}
```

### Resource Optimization
```
GET /api/ai/resource-optimization
```
**Response:**
```json
{
  "optimizations": [
    {
      "area": "Ward 5",
      "current_routes": 4,
      "optimized_routes": 3,
      "distance_reduction_percent": 17,
      "cost_savings_percent": 14,
      "teams_recommended": 2,
      "efficiency_gain": 15.5
    }
  ],
  "stats": {
    "total_areas_optimized": 10,
    "avg_distance_reduction": 16.5,
    "avg_cost_savings": 14.2
  }
}
```

### Data Ingestion Status
```
GET /api/ai/data-ingestion
```
**Response:**
```json
{
  "sources": [
    {
      "name": "BBMP Grievance Portal",
      "records": 12458,
      "status": "healthy",
      "last_sync": "2 hours ago"
    }
  ],
  "stats": {
    "total_sources": 6,
    "healthy_sources": 5,
    "degraded_sources": 1,
    "total_records_ingested": 78800,
    "ingestion_rate": "1.2M records/hour"
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "error": "Endpoint not found"
}
```

### 500 Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Authentication (Future)

Once authentication is implemented, include:
```
Authorization: Bearer {token}
```

---

## Rate Limiting (Future)

Rate limits per endpoint:
- Health endpoints: Unlimited
- Dashboard endpoints: 100 requests/minute
- Complaint endpoints: 100 requests/minute
- AI endpoints: 50 requests/minute
