"""
Fraud Detector Implementation - UrbanPulse AI
Uses Isolation Forest to detect anomalies in complaint closure patterns:
1. Fast closures
2. Repeated reopenings
3. Suspicious repair patterns
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import logging
from typing import Dict, List, Any, Optional, Tuple
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComplaintFraudDetector:
    """
    Detects fake complaint closures and suspicious activity using Isolation Forest.
    """
    
    def __init__(self, contamination: float = 0.05):
        """
        Initialize detector.
        contamination: percentage of data expected to be outliers.
        """
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.is_trained = False
        
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features for fraud detection:
        - closure_duration_hours: Time from report to resolution
        - reopening_count: Number of times complaint was reopened (simulated if missing)
        - staff_resolution_count: Count of complaints resolved by same staff in same day
        - severity: High severity + Low duration = Suspicious
        """
        # Ensure timestamp columns are datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Simulated features since raw data is static
        # In production, these would be calculated from event logs
        np.random.seed(42)
        
        # 1. Closure duration (Simulated for this sample)
        # Usually between 2h to 240h (10 days)
        df['closure_duration_hours'] = np.random.exponential(scale=48, size=len(df))
        
        # 2. Reopening count (0 for 90%, 1-3 for others)
        df['reopening_count'] = np.random.choice([0, 1, 2, 3], size=len(df), p=[0.9, 0.06, 0.03, 0.01])
        
        # 3. Staff resolution intensity
        # Count closures by staff per day
        # For simplicity, using a random resolution speed factor
        df['resolution_speed_factor'] = df['closure_duration_hours'] / (df['severity'] + 1)
        
        features = df[['closure_duration_hours', 'reopening_count', 'severity', 'resolution_speed_factor']]
        return features.fillna(0)

    def train(self, data_path: str):
        """Train Isolation Forest on historical data."""
        logger.info(f"Loading data from {data_path} for fraud detection training")
        df = pd.read_csv(data_path).head(5000) # Sample for performance
        X = self.prepare_features(df)
        
        logger.info("Fitting Isolation Forest model...")
        self.model.fit(X)
        self.is_trained = True
        logger.info("Fraud detection model trained.")

    def get_fraud_score(self, closure_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate fraud/anomaly score for a single closure event.
        Returns score (0-1) where higher is more suspicious.
        """
        # Prepare input
        X_input = pd.DataFrame([{
            'closure_duration_hours': closure_data.get('duration_hours', 48),
            'reopening_count': closure_data.get('reopenings', 0),
            'severity': closure_data.get('severity', 3),
            'resolution_speed_factor': closure_data.get('duration_hours', 48) / (closure_data.get('severity', 3) + 1)
        }])
        
        if not self.is_trained:
            # Heuristic fallback if model not trained
            score = 0.0
            if X_input['closure_duration_hours'].iloc[0] < 1 and X_input['severity'].iloc[0] > 4:
                score = 0.9 # Fast closure of high severity = Ultra suspicious
            elif X_input['reopening_count'].iloc[0] >= 3:
                score = 0.8
            return {"fraud_score": score, "is_anomaly": score > 0.7, "reason": "Heuristic fallback"}

        # decision_function returns anomaly score (lower is more anomalous)
        # we invert it for a 0-1 "fraud score"
        raw_score = self.model.decision_function(X_input)[0]
        # Map (-0.5, 0.5) to (1, 0)
        fraud_score = np.clip(0.5 - raw_score, 0, 1)
        
        is_anomaly = self.model.predict(X_input)[0] == -1
        
        reasons = []
        if X_input['closure_duration_hours'].iloc[0] < 2: reasons.append("Ultra-fast closure")
        if X_input['reopening_count'].iloc[0] > 1: reasons.append("Multiple reopenings")
        
        return {
            "fraud_score": float(fraud_score),
            "is_anomaly": bool(is_anomaly),
            "reasons": reasons,
            "risk_level": "Critical" if fraud_score > 0.7 else "Elevated" if fraud_score > 0.4 else "Normal"
        }

if __name__ == "__main__":
    detector = ComplaintFraudDetector()
    # Test cases
    test_cases = [
        {"duration_hours": 0.5, "reopenings": 0, "severity": 5}, # Suspicious: Fast+High Severity
        {"duration_hours": 72, "reopenings": 4, "severity": 3},  # Suspicious: Many reopenings
        {"duration_hours": 48, "reopenings": 0, "severity": 2}   # Normal
    ]
    for tc in test_cases:
        print(f"Test {tc}: {detector.get_fraud_score(tc)}")

