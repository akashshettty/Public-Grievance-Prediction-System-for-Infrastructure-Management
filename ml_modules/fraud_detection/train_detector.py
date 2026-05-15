"""
Training Script for Fraud Detection
Uses Isolation Forest to identify anomalous complaint closure behaviors.
"""

import pandas as pd
import joblib
import os
import sys
import logging

# Add root to sys path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ml_modules.fraud_detection.detector import ComplaintFraudDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_fraud_model():
    data_path = "data/processed/grievances_cleaned.csv"
    if not os.path.exists(data_path):
        logger.error(f"Data not found at {data_path}")
        return

    # 1. Initialize detector
    detector = ComplaintFraudDetector(contamination=0.05)
    
    # 2. Train
    logger.info("Starting training of Fraud Detection model (Isolation Forest)...")
    detector.train(data_path)
    
    # 3. Save model
    model_dir = "models/fraud_detection"
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(detector.model, f"{model_dir}/isolation_forest.joblib")
    logger.info(f"Model saved to {model_dir}/isolation_forest.joblib")

    # 4. Verification test
    logger.info("Running verification test...")
    sample_closure = {"duration_hours": 0.2, "reopenings": 0, "severity": 5}
    result = detector.get_fraud_score(sample_closure)
    print(f"Sample suspicious closure detection: {result}")

if __name__ == "__main__":
    train_fraud_model()
