"""
Training Script for Infrastructure Failure Prediction
Uses Random Forest to correlate complaints, weather, and age with failure risk.
"""

import pandas as pd
import os
import logging
import sys
from pathlib import Path

# Add root to sys path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from ml_modules.forecasting.predictor import InfrastructureFailurePredictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_training():
    data_path = "data/processed/grievances_cleaned.csv"
    if not os.path.exists(data_path):
        logger.error(f"Data not found at {data_path}")
        return

    predictor = InfrastructureFailurePredictor()
    
    logger.info("Initializing training for Infrastructure Failure Prediction...")
    predictor.train_risk_model(data_path)
    
    # Save the model (simplified for demo)
    import joblib
    model_path = "models/forecasting/rf_failure_model.joblib"
    os.makedirs("models/forecasting", exist_ok=True)
    joblib.dump(predictor.rf_model, model_path)
    logger.info(f"Model saved to {model_path}")

    # Test on a few wards
    df = pd.read_csv(data_path)
    top_wards = df['kgis_ward_name'].value_counts().head(5).index.tolist()
    
    logger.info("Generating sample predictions for top wards...")
    for ward in top_wards:
        ward_data = df[df['kgis_ward_name'] == ward]
        recent_stats = {
            'complaint_count': len(ward_data.tail(30)),
            'avg_severity': ward_data['severity'].mean(),
            'prev_day_count': 5,
            'rolling_7d_count': 8,
            'road_age_years': 8,
            'repair_delay_days': 15
        }
        prediction = predictor.get_failure_probability(recent_stats)
        print(f"Ward: {ward} | Risk: {prediction['risk_level']} ({prediction['risk_score']:.2f}) | Type: {prediction['predicted_failure_type']}")

if __name__ == "__main__":
    run_training()
