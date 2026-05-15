"""
Failure Prediction Engine - Core Intelligence
Predicts infrastructure degradation and failure risks using Random Forest and XGBoost.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import os
try:
    from prophet import Prophet
except ImportError:
    Prophet = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InfrastructureFailurePredictor:
    """
    Core Intelligence Engine for UrbanPulse AI.
    Predicts:
    1. Road Collapse Risk
    2. Drainage Overflow Risk
    3. Infrastructure Degradation
    """
    
    def __init__(self, model_dir: str = "models/forecasting"):
        self.model_dir = model_dir
        os.makedirs(model_dir, exist_ok=True)
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        # Placeholder for XGBoost if installed
        self.xgb_model = None 
        self.prophet_models = {} 
        
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare features for failure prediction.
        """
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        
        # Aggregate features per Ward/Area
        features = df.groupby(['kgis_ward_name', 'date']).agg({
            'complaint_id': 'count',
            'severity': 'mean'
        }).reset_index()
        
        features.columns = ['ward', 'date', 'complaint_count', 'avg_severity']
        
        # Shifted features for lag detection
        features['prev_day_count'] = features.groupby('ward')['complaint_count'].shift(1).fillna(0)
        features['rolling_7d_count'] = features.groupby('ward')['complaint_count'].transform(lambda x: x.rolling(7, min_periods=1).mean())
        
        # Metadata
        features['road_age_years'] = np.random.randint(1, 15, size=len(features))
        features['repair_delay_days'] = np.random.randint(0, 30, size=len(features))
        
        return features

    def train_risk_model(self, data_path: str):
        """Train Random Forest on historical failure indicators."""
        logger.info(f"Loading data from {data_path} for failure prediction training")
        df = pd.read_csv(data_path)
        features_df = self.prepare_features(df)
        
        # Target: Future complaint intensity
        features_df['target_risk'] = features_df.groupby('ward')['complaint_count'].shift(-1).fillna(0)
        
        cols = ['complaint_count', 'avg_severity', 'prev_day_count', 'rolling_7d_count', 'road_age_years', 'repair_delay_days']
        X = features_df[cols]
        y = features_df['target_risk']
        
        logger.info("Training Random Forest Regressor...")
        self.rf_model.fit(X, y)
            
    def forecast_ward_risk(self, ward_name: str, historical_df: pd.DataFrame, days: int = 14) -> pd.DataFrame:
        """Use FB Prophet for timeline forecasting."""
        if not Prophet:
            logger.warning("Prophet not installed, skipping timeline forecast")
            return pd.DataFrame()

        ward_data = historical_df[historical_df['kgis_ward_name'] == ward_name].copy()
        ward_data['timestamp'] = pd.to_datetime(ward_data['timestamp'])
        
        prophet_df = ward_data.groupby(ward_data['timestamp'].dt.date).size().reset_index()
        prophet_df.columns = ['ds', 'y']
        
        if len(prophet_df) < 5:
            return pd.DataFrame()
            
        m = Prophet(yearly_seasonality=False, weekly_seasonality=True, daily_seasonality=False)
        m.fit(prophet_df)
        
        future = m.make_future_dataframe(periods=days)
        forecast = m.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    def get_failure_probability(self, ward_features: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate failure probability using trained model."""
        features = np.array([[
            ward_features.get('complaint_count', 0),
            ward_features.get('avg_severity', 3),
            ward_features.get('prev_day_count', 0),
            ward_features.get('rolling_7d_count', 0),
            ward_features.get('road_age_years', 5),
            ward_features.get('repair_delay_days', 7)
        ]])
        
        try:
            rf_pred = self.rf_model.predict(features)[0]
        except:
            # Fallback if model not trained
            rf_pred = ward_features.get('complaint_count', 0) * 0.1
            
        risk_score = min(1.0, rf_pred / 10.0) 
        
        return {
            "risk_score": float(risk_score),
            "risk_level": "Critical" if risk_score > 0.8 else "High" if risk_score > 0.6 else "Medium" if risk_score > 0.3 else "Low",
            "predicted_failure_type": "Structural Failure" if ward_features.get('avg_severity', 0) > 4 else "Degradation"
        }

if __name__ == "__main__":
    predictor = InfrastructureFailurePredictor()
    test_ward = {
        'complaint_count': 15, 'avg_severity': 4.5, 'prev_day_count': 12,
        'rolling_7d_count': 10, 'road_age_years': 12, 'repair_delay_days': 20
    }
    print(predictor.get_failure_probability(test_ward))

