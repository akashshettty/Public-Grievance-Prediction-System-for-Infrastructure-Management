"""Shared data models for API responses."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class ComplaintModel:
    """Complaint data model."""
    id: str
    description: str
    area: str
    issue_type: str
    status: str
    severity: float
    created_at: datetime
    closed_at: Optional[datetime] = None


@dataclass
class RiskScoreModel:
    """Risk score data model."""
    area: str
    risk_level: str
    risk_score: float
    last_updated: datetime


@dataclass
class APIResponseModel:
    """Standard API response model."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
