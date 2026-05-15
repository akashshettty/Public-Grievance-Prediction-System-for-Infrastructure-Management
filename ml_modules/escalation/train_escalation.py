"""
Training Script for Escalation Prediction
Trains Random Forest and XGBoost to detect complaints at risk of viral escalation.
"""

import pandas as pd
import joblib
import os
import sys
import logging

# Add root to sys path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ml_modules.escalation.predictor import ComplaintEscalationPredictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_escalation_model():
    data_path = "data/processed/grievances_cleaned.csv"
    if not os.path.exists(data_path):
        logger.error(f"Data not found at {data_path}")
        return

    # 1. Initialize predictor
    predictor = ComplaintEscalationPredictor()
    
    # 2. Train
    logger.info("Starting training of Escalation Prediction models...")
    predictor.train(data_path)
    
    # 3. Save models
    model_dir = "models/escalation"
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(predictor.rf_model, f"{model_dir}/rf_escalation.joblib")
    if predictor.xgb_model:
        joblib.dump(predictor.xgb_model, f"{model_dir}/xgb_escalation.joblib")
        
    logger.info(f"Models saved to {model_dir}")

    # 4. Verification test
    logger.info("Running verification test...")
    sample_risk = {"days_unresolved": 15, "ward_recurrence": 12, "severity": 5, "sentiment_score": 0.15}
    result = predictor.get_escalation_risk(sample_risk)
    print(f"Sample escalation risk detection: {result}")

if __name__ == "__main__":
    train_escalation_model()
