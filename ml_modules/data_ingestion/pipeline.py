import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InfrastructureDataPipeline:
    """
    Phase 2: Data Ingestion Engine
    Handles multi-source integration for Infrastructure Intelligence.
    """
    
    def __init__(self, data_dir="data/processed"):
        self.data_dir = data_dir
        self.master_df = None
        
    def load_base_grievances(self):
        """Loads the cleaned grievance data."""
        path = os.path.join(self.data_dir, "grievances_cleaned.csv")
        if os.path.exists(path):
            return pd.read_csv(path)
        else:
            logger.error(f"Base data not found at {path}")
            return None

    def simulate_weather_data(self, dates):
        """Simulates historical weather data for correlation."""
        weather_conditions = ['Clear', 'Cloudy', 'Rain', 'Heavy Rain', 'Thunderstorm']
        return pd.DataFrame({
            'date': dates,
            'rainfall_mm': np.random.gamma(2, 5, len(dates)),
            'humidity': np.random.uniform(40, 95, len(dates)),
            'condition': np.random.choice(weather_conditions, len(dates))
        })

    def simulate_traffic_data(self, dates):
        """Simulates traffic congestion metrics."""
        return pd.DataFrame({
            'date': dates,
            'congestion_index': np.random.uniform(0.1, 1.0, len(dates)),
            'avg_speed': np.random.uniform(10, 45, len(dates))
        })

    def execute_etl(self):
        """Standardizes and merges all data sources."""
        logger.info("Starting Multi-Source ETL Pipeline...")
        
        # 1. Load Primary Data
        df = self.load_base_grievances()
        if df is None: return
        
        # Ensure date format - Using 'timestamp' as found in grievances_cleaned.csv
        date_col = 'timestamp' if 'timestamp' in df.columns else 'CreatedDate'
        df[date_col] = pd.to_datetime(df[date_col])
        unique_dates = df[date_col].dt.date.unique()
        
        # 2. Ingest External Intelligence
        logger.info("Ingesting Weather and Traffic Intelligence...")
        weather_df = self.simulate_weather_data(unique_dates)
        traffic_df = self.simulate_traffic_data(unique_dates)
        
        # 3. Merge Intelligence Layers
        df['date_only'] = df[date_col].dt.date
        
        # Join Weather
        df = df.merge(weather_df, left_on='date_only', right_on='date', how='left')
        
        # Join Traffic
        df = df.merge(traffic_df, left_on='date_only', right_on='date', how='left')
        
        # 4. Feature Engineering: Risk Correlation
        # Higher rainfall + specific complaint types = higher risk
        category_col = 'category' if 'category' in df.columns else 'Category'
        df['flood_risk_score'] = (df['rainfall_mm'] * 0.7) + (df[category_col].apply(lambda x: 10 if x in ['Rain Water Stagnation', 'Flooding', 'Storm Water Drain'] else 0))
        
        # 5. Save Merged Intelligence Master
        output_name = "infrastructure_intelligence_master.csv"
        output_path = os.path.join(self.data_dir, output_name)
        df.drop(columns=['date_x', 'date_y', 'date_only'], inplace=True, errors='ignore')
        df.to_csv(output_path, index=False)
        
        self.master_df = df
        logger.info(f"ETL Complete. Master dataset saved with {len(df)} records and {len(df.columns)} features.")
        return output_path

if __name__ == "__main__":
    pipeline = InfrastructureDataPipeline()
    pipeline.execute_etl()

