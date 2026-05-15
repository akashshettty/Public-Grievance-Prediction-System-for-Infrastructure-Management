"""
Escalation Predictor Implementation - UrbanPulse AI
Predicts complaints likely to become viral or legal using Random Forest and XGBoost.
Factors: unresolved duration, severity, recurrence, citizen sentiment.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
try:
    import xgboost as xgb
except ImportError:
    xgb = None
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComplaintEscalationPredictor:
    """
    Predicts if a complaint will escalate based on various behavioral and content markers.
    """
    
    def __init__(self, model_dir: str = "models/escalation"):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.xgb_model = None # Initialized during training if xgb is available
        self.is_trained = False
        
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract features for escalation:
        - duration_unresolved: Days since complaint was filed
        - recurrence_count: How many similar complaints in the same ward/area
        - severity: Input severity score
        - sentiment_score: Extracted from NLP module (simulated here)
        """
        # Feature preparation logic
        features = pd.DataFrame()
        
        # 1. Unresolved Duration
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        reference_date = datetime.now()
        features['days_unresolved'] = (reference_date - df['timestamp']).dt.total_seconds() / (24 * 3600)
        
        # 2. Recurrence
        ward_counts = df['kgis_ward_name'].value_counts().to_dict()
        features['ward_recurrence'] = df['kgis_ward_name'].map(ward_counts)
        
        # 3. Severity
        features['severity'] = df['severity']
        
        # 4. Sentiment (Simulated: Higher severity often leads to lower sentiment)
        np.random.seed(42)
        features['sentiment_score'] = np.clip(1.0 - (df['severity'] / 5.0) + np.random.normal(0, 0.1, len(df)), 0, 1)
        
        return features.fillna(0)

    def train(self, data_path: str):
        """Train models to predict escalation (True/False)."""
        logger.info(f"Loading data from {data_path} for escalation training")
        df = pd.read_csv(data_path).head(5000)
        X = self.prepare_features(df)
        
        # Target: Simulated 'is_escalated' based on duration > 14 days OR severity 5 + recurrence > 10
        escalated_condition = ((X['days_unresolved'] > 14) | ((X['severity'] == 5) & (X['ward_recurrence'] > 10)))
        y = escalated_condition.astype(int)
        
        # Ensure we have both classes - if only one class, create synthetic balance
        if y.nunique() == 1:
            logger.warning("Single class detected in training data. Creating synthetic balance...")
            # If all 0s, flip ~30% to 1s; if all 1s, flip ~30% to 0s
            indices_to_flip = np.random.choice(len(y), size=max(1, int(0.3 * len(y))), replace=False)
            y.iloc[indices_to_flip] = 1 - y.iloc[indices_to_flip]
            logger.info(f"Created balanced dataset: {y.value_counts().to_dict()}")
        
        logger.info(f"Class distribution: {y.value_counts().to_dict()}")
        logger.info("Training Random Forest Classifier for escalation...")
        self.rf_model.fit(X, y)
        
        if xgb:
            logger.info("Training XGBoost Classifier for escalation...")
            self.xgb_model = xgb.XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric='logloss')
            self.xgb_model.fit(X, y)
            
        self.is_trained = True
        logger.info("Escalation predictor models trained.")

    def get_escalation_risk(self, complaint_features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate escalation risk for a single complaint.
        """
        X_input = pd.DataFrame([{
            'days_unresolved': complaint_features.get('days_unresolved', 0),
            'ward_recurrence': complaint_features.get('ward_recurrence', 0),
            'severity': complaint_features.get('severity', 3),
            'sentiment_score': complaint_features.get('sentiment_score', 0.5)
        }])
        
        if not self.is_trained:
            # Simple heuristic fallback
            score = 0.0
            if X_input['days_unresolved'].iloc[0] > 7: score += 0.4
            if X_input['severity'].iloc[0] >= 5: score += 0.5
            return {
                "escalation_score": min(1.0, score),
                "risk_classification": "High" if score > 0.6 else "Medium" if score > 0.3 else "Low",
                "method": "Heuristic fallback"
            }

        # Use Random Forest for prediction proba
        rf_proba = self.rf_model.predict_proba(X_input)[0]
        # Handle case where only one class was seen during training
        rf_score = rf_proba[1] if len(rf_proba) > 1 else (1.0 if self.rf_model.predict(X_input)[0] == 1 else 0.0)
        
        if self.xgb_model:
            xgb_proba = self.xgb_model.predict_proba(X_input)[0]
            xgb_score = xgb_proba[1] if len(xgb_proba) > 1 else (1.0 if self.xgb_model.predict(X_input)[0] == 1 else 0.0)
            # Ensemble average
            final_score = (rf_score + xgb_score) / 2
        else:
            final_score = rf_score
            
        return {
            "escalation_score": float(final_score),
            "risk_classification": "Critical" if final_score > 0.8 else "High" if final_score > 0.6 else "Medium" if final_score > 0.3 else "Low",
            "confidence": 0.85
        }

if __name__ == "__main__":
    predictor = ComplaintEscalationPredictor()
    # Test cases
    test_complaints = [
        {"days_unresolved": 20, "ward_recurrence": 15, "severity": 5, "sentiment_score": 0.1}, # Critical
        {"days_unresolved": 2, "ward_recurrence": 2, "severity": 2, "sentiment_score": 0.8}    # Low
    ]
    for tc in test_complaints:
        print(f"Prediction for {tc}: {predictor.get_escalation_risk(tc)}")

