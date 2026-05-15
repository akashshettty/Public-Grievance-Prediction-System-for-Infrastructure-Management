"""
Data Service
Handles data loading, caching, and preprocessing.
"""

import pandas as pd
from pathlib import Path
from functools import lru_cache
from typing import Optional, Dict, Any
from backend.config import get_config

config = get_config()


class DataService:
    """Service for managing data loading and caching."""
    
    _instance = None
    _data_cache = {}
    
    def __new__(cls):
        """Singleton pattern to ensure single instance."""
        if cls._instance is None:
            cls._instance = super(DataService, cls).__new__(cls)
        return cls._instance
    
    @staticmethod
    def load_csv(file_path: Path) -> pd.DataFrame:
        """
        Load CSV file with error handling.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Pandas DataFrame
        """
        try:
            if file_path.exists():
                return pd.read_csv(file_path)
            return pd.DataFrame()
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return pd.DataFrame()
    
    def get_grievances_data(self) -> pd.DataFrame:
        """Get cleaned grievance data."""
        if "grievances" not in self._data_cache:
            self._data_cache["grievances"] = self.load_csv(config.CLEAN_DATA_PATH)
        return self._data_cache["grievances"].copy()
    
    def get_risk_data(self) -> pd.DataFrame:
        """Get risk scores data."""
        if "risk" not in self._data_cache:
            self._data_cache["risk"] = self.load_csv(config.RISK_DATA_PATH)
        return self._data_cache["risk"].copy()
    
    def get_hotspot_data(self) -> pd.DataFrame:
        """Get hotspot predictions data."""
        if "hotspot" not in self._data_cache:
            self._data_cache["hotspot"] = self.load_csv(config.HOTSPOT_DATA_PATH)
        return self._data_cache["hotspot"].copy()
    
    def get_area_features(self) -> pd.DataFrame:
        """Get area features data."""
        if "area_features" not in self._data_cache:
            self._data_cache["area_features"] = self.load_csv(config.AREA_FEATURES_PATH)
        return self._data_cache["area_features"].copy()
    
    def clear_cache(self):
        """Clear all cached data."""
        self._data_cache.clear()
    
    def refresh_data(self):
        """Refresh all cached data from disk."""
        self.clear_cache()
