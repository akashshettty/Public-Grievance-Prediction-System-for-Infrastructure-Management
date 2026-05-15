"""
Weather API Connector for UrbanPulse AI
Fetches weather data for infrastructure prediction
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
from pathlib import Path


class WeatherConnector:
    """Connector for weather data APIs and caching"""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path("data/raw/weather_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.bengaluru_coords = {"latitude": 12.9716, "longitude": 77.5946}
    
    def generate_simulated_weather_data(
        self, 
        start_date: datetime, 
        end_date: datetime,
        ward_list: List[str]
    ) -> pd.DataFrame:
        """
        Generate realistic simulated weather data for Bengaluru wards
        
        Args:
            start_date: Start date for simulation
            end_date: End date for simulation
            ward_list: List of ward names
            
        Returns:
            DataFrame with weather data
        """
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        weather_records = []
        
        np.random.seed(42)
        
        for date in dates:
            # Simulate seasonal patterns for Bengaluru
            month = date.month
            
            # Temperature varies with season
            if month in [4, 5]:  # Summer
                base_temp = 35 + np.random.normal(0, 2)
            elif month in [6, 7, 8, 9]:  # Monsoon
                base_temp = 28 + np.random.normal(0, 2)
            else:  # Winter/Post-monsoon
                base_temp = 25 + np.random.normal(0, 1.5)
            
            # Rainfall likelihood increases during monsoon
            if month in [6, 7, 8, 9]:
                rainfall = np.random.exponential(scale=15) if np.random.random() > 0.3 else 0
                humidity = 75 + np.random.normal(0, 5)
            else:
                rainfall = 0 if np.random.random() > 0.1 else np.random.exponential(scale=10)
                humidity = 55 + np.random.normal(0, 8)
            
            # Wind speed
            wind_speed = np.random.exponential(scale=8)
            
            for ward in ward_list:
                weather_records.append({
                    'date': date,
                    'ward': ward,
                    'temperature': base_temp,
                    'rainfall_mm': max(0, rainfall),
                    'humidity_percent': min(100, max(0, humidity)),
                    'wind_speed_kmh': wind_speed,
                    'pressure_hpa': 1013 + np.random.normal(0, 2),
                    'visibility_km': 10 - rainfall * 0.1 + np.random.normal(0, 0.5),
                    'is_monsoon_season': month in [6, 7, 8, 9]
                })
        
        df = pd.DataFrame(weather_records)
        return df
    
    def fetch_real_weather_data(self, api_key: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch real weather data from API (OpenWeatherMap, etc.)
        Currently returns simulated data as fallback
        
        Args:
            api_key: API key for weather service
            
        Returns:
            DataFrame with weather data
        """
        # TODO: Implement real API calls to OpenWeatherMap, NOAA, or similar
        # For now, generate simulated data
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()
        
        return self.generate_simulated_weather_data(
            start_date, 
            end_date, 
            ["Ward 1", "Ward 2", "Ward 3"]  # Placeholder
        )
    
    def cache_weather_data(self, df: pd.DataFrame, cache_name: str) -> None:
        """Cache weather data locally"""
        cache_file = self.cache_dir / f"{cache_name}.csv"
        df.to_csv(cache_file, index=False)
    
    def load_cached_weather_data(self, cache_name: str) -> Optional[pd.DataFrame]:
        """Load cached weather data"""
        cache_file = self.cache_dir / f"{cache_name}.csv"
        if cache_file.exists():
            return pd.read_csv(cache_file, parse_dates=['date'])
        return None


class WeatherEnricher:
    """Enriches complaint data with weather context"""
    
    def __init__(self, weather_df: pd.DataFrame):
        self.weather_df = weather_df.copy()
        self.weather_df['date'] = pd.to_datetime(self.weather_df['date']).dt.date
    
    def enrich_complaints(self, complaints_df: pd.DataFrame) -> pd.DataFrame:
        """
        Add weather features to complaint data
        
        Args:
            complaints_df: DataFrame with complaints
            
        Returns:
            DataFrame with weather features added
        """
        df = complaints_df.copy()
        df['complaint_date'] = pd.to_datetime(df['timestamp']).dt.date
        
        # Merge with weather data
        df = df.merge(
            self.weather_df,
            left_on=['area', 'complaint_date'],
            right_on=['ward', 'date'],
            how='left'
        )
        
        # Fill missing weather data with averages
        numeric_cols = ['temperature', 'rainfall_mm', 'humidity_percent', 'wind_speed_kmh']
        for col in numeric_cols:
            if col in df.columns:
                df[col].fillna(df[col].mean(), inplace=True)
        
        return df
