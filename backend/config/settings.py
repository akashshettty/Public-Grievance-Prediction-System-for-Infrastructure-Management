"""
Backend Configuration Settings
Handles environment-specific configurations.
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


class BaseConfig:
    """Base configuration with common settings."""
    
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # API settings
    API_TITLE = "UrbanPulse AI API"
    API_VERSION = "2.0.0"
    API_DESCRIPTION = "Smart city infrastructure management and complaint analytics"
    
    # CORS settings
    CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5000", "*"]
    
    # Data paths
    PROJECT_ROOT = PROJECT_ROOT
    DATA_DIR = DATA_DIR
    PROCESSED_DATA_DIR = PROCESSED_DATA_DIR
    
    # Data file paths
    CLEAN_DATA_PATH = PROCESSED_DATA_DIR / "grievances_cleaned.csv"
    RISK_DATA_PATH = PROCESSED_DATA_DIR / "area_risk_scores.csv"
    HOTSPOT_DATA_PATH = PROCESSED_DATA_DIR / "hotspot_predictions.csv"
    AREA_FEATURES_PATH = PROCESSED_DATA_DIR / "area_features.csv"
    
    # Cache settings
    CACHE_ENABLED = True
    CACHE_TIMEOUT = 300  # 5 minutes
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    
    DEBUG = True
    TESTING = False
    LOG_LEVEL = "DEBUG"


class ProductionConfig(BaseConfig):
    """Production environment configuration."""
    
    DEBUG = False
    TESTING = False
    LOG_LEVEL = "WARNING"


class TestingConfig(BaseConfig):
    """Testing environment configuration."""
    
    DEBUG = True
    TESTING = True
    LOG_LEVEL = "DEBUG"


def get_config(env=None):
    """
    Get configuration object based on environment.
    
    Args:
        env (str): Environment name ('development', 'production', 'testing')
        
    Returns:
        Configuration object
    """
    if env is None:
        env = os.getenv("FLASK_ENV", "development")
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    
    return config_map.get(env, DevelopmentConfig)
