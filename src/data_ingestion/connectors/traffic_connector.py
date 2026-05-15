"""
Traffic Density Connector for UrbanPulse AI
Provides traffic congestion data for infrastructure analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path


class TrafficConnector:
    """Connector for traffic density data"""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path("data/raw/traffic_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_simulated_traffic_data(
        self,
        start_date: datetime,
        end_date: datetime,
        ward_list: List[str]
    ) -> pd.DataFrame:
        """
        Generate realistic traffic density data for wards
        
        Traffic density factors:
        - Day of week (weekends lower, weekdays higher)
        - Time of day (peak hours vs off-peak)
        - Ward characteristics (commercial vs residential)
        """
        np.random.seed(42)
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        traffic_records = []
        
        # Ward characteristics (commercial areas have higher traffic)
        commercial_wards = {'Ward 1', 'Ward 5', 'Ward 12', 'Ward 20'}
        
        for date in dates:
            hour = date.hour
            day_of_week = date.dayofweek  # 0=Monday, 6=Sunday
            
            # Peak hours: 7-9 AM, 5-7 PM (weekdays)
            is_peak_hour = (hour in [7, 8, 9, 17, 18, 19]) and day_of_week < 5
            is_evening = hour in [17, 18, 19]
            
            for ward in ward_list:
                is_commercial = ward in commercial_wards
                
                # Base traffic depends on ward type
                base_traffic = 70 if is_commercial else 50
                
                # Peak hour multiplier
                if is_peak_hour:
                    traffic_density = base_traffic + np.random.normal(20, 5)
                elif hour in [10, 11, 12, 13, 14, 15, 16]:
                    traffic_density = base_traffic + np.random.normal(10, 3)
                elif hour < 6 or hour > 22:
                    traffic_density = base_traffic - 30 + np.random.normal(5, 2)
                else:
                    traffic_density = base_traffic + np.random.normal(5, 3)
                
                # Lower traffic on weekends
                if day_of_week >= 5:
                    traffic_density *= 0.7
                
                traffic_density = max(5, min(100, traffic_density))
                
                traffic_records.append({
                    'timestamp': date,
                    'ward': ward,
                    'traffic_density_percent': traffic_density,
                    'congestion_level': self._classify_congestion(traffic_density),
                    'is_peak_hour': is_peak_hour,
                    'day_of_week': day_of_week,
                    'hour': hour
                })
        
        return pd.DataFrame(traffic_records)
    
    @staticmethod
    def _classify_congestion(density: float) -> str:
        """Classify traffic density into levels"""
        if density < 30:
            return 'low'
        elif density < 60:
            return 'moderate'
        elif density < 85:
            return 'high'
        else:
            return 'severe'
    
    def fetch_real_traffic_data(self) -> pd.DataFrame:
        """
        Fetch real traffic data from Google Maps, HERE, or Inrix APIs
        Currently returns simulated data
        """
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        
        return self.generate_simulated_traffic_data(
            start_date,
            end_date,
            ["Ward 1", "Ward 2", "Ward 3"]
        )
    
    def cache_traffic_data(self, df: pd.DataFrame, cache_name: str) -> None:
        """Cache traffic data"""
        cache_file = self.cache_dir / f"{cache_name}.csv"
        df.to_csv(cache_file, index=False)
    
    def load_cached_traffic_data(self, cache_name: str) -> Optional[pd.DataFrame]:
        """Load cached traffic data"""
        cache_file = self.cache_dir / f"{cache_name}.csv"
        if cache_file.exists():
            return pd.read_csv(cache_file, parse_dates=['timestamp'])
        return None


class TrafficEnricher:
    """Enriches complaint data with traffic context"""
    
    def __init__(self, traffic_df: pd.DataFrame):
        self.traffic_df = traffic_df.copy()
    
    def enrich_complaints(self, complaints_df: pd.DataFrame) -> pd.DataFrame:
        """
        Add traffic features to complaint data
        
        Args:
            complaints_df: DataFrame with complaints
            
        Returns:
            DataFrame with traffic features added
        """
        df = complaints_df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Aggregate traffic data to daily level for complaints
        traffic_daily = self.traffic_df.copy()
        traffic_daily['date'] = pd.to_datetime(traffic_daily['timestamp']).dt.date
        traffic_daily = traffic_daily.groupby(['ward', 'date']).agg({
            'traffic_density_percent': 'mean',
            'congestion_level': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'moderate'
        }).reset_index()
        
        df['complaint_date'] = pd.to_datetime(df['timestamp']).dt.date
        
        # Merge with traffic data
        df = df.merge(
            traffic_daily,
            left_on=['area', 'complaint_date'],
            right_on=['ward', 'date'],
            how='left'
        )
        
        # Fill missing values
        df['traffic_density_percent'].fillna(df['traffic_density_percent'].median(), inplace=True)
        df['congestion_level'].fillna('moderate', inplace=True)
        
        return df
