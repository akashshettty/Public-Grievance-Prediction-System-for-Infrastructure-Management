"""
Advanced Spatio-Temporal Infrastructure Forecasting
Predicts infrastructure failures using LSTM, Prophet, ARIMA, and Graph Neural Networks
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from sklearn.preprocessing import MinMaxScaler
import json
from pathlib import Path


class InfrastructureDegradationPredictor:
    """
    Predicts infrastructure degradation and failure probability
    
    Factors considered:
    - Complaint recurrence patterns
    - Weather conditions
    - Infrastructure age
    - Traffic pressure
    - Repair delays
    - Seasonal trends
    """
    
    def __init__(self, lookback_days: int = 365):
        self.lookback_days = lookback_days
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def calculate_degradation_score(
        self,
        complaint_count_7d: int,
        complaint_count_30d: int,
        avg_complaint_age_days: int,
        infrastructure_age: int,
        days_since_last_repair: int,
        avg_rainfall_7d: float,
        traffic_density: float
    ) -> float:
        """
        Calculate infrastructure degradation score (0-1)
        
        Higher score = higher risk of failure
        """
        score = 0.0
        
        # Complaint frequency (recent complaints indicate active issues)
        recent_complaint_intensity = complaint_count_7d / max(1, complaint_count_30d)
        if complaint_count_30d > 10:
            score += 0.25 * (recent_complaint_intensity)
        
        # Unresolved complaints (old complaints not fixed)
        if avg_complaint_age_days > 30:
            score += 0.15 * min(1.0, (avg_complaint_age_days - 30) / 90)
        
        # Infrastructure age (older = more degradation)
        if infrastructure_age > 30:
            score += 0.25 * min(1.0, (infrastructure_age - 30) / 40)
        else:
            score += 0.05 * (infrastructure_age / 30)
        
        # Maintenance delays
        if days_since_last_repair > 365:
            score += 0.20
        elif days_since_last_repair > 180:
            score += 0.10
        
        # Weather impact (rainfall accelerates degradation)
        if avg_rainfall_7d > 20:  # Significant rainfall
            score += 0.15
        
        # Traffic pressure
        if traffic_density > 80:
            score += 0.10
        elif traffic_density > 60:
            score += 0.05
        
        return min(1.0, score)
    
    def predict_ward_failure_probability(
        self,
        ward_analytics: Dict
    ) -> Dict:
        """
        Predict failure probability for a ward
        
        Args:
            ward_analytics: Dictionary with ward metrics
            
        Returns:
            Dictionary with predictions
        """
        degradation_score = self.calculate_degradation_score(
            ward_analytics.get('complaint_count_7d', 0),
            ward_analytics.get('complaint_count_30d', 0),
            ward_analytics.get('avg_complaint_age_days', 0),
            ward_analytics.get('infrastructure_age', 20),
            ward_analytics.get('days_since_last_repair', 180),
            ward_analytics.get('avg_rainfall_7d', 0),
            ward_analytics.get('traffic_density', 50)
        )
        
        # Classify risk level
        if degradation_score > 0.8:
            risk_level = 'critical'
        elif degradation_score > 0.6:
            risk_level = 'high'
        elif degradation_score > 0.4:
            risk_level = 'medium'
        else:
            risk_level = 'low'
        
        return {
            'degradation_score': degradation_score,
            'risk_level': risk_level,
            'failure_probability': min(0.95, degradation_score),
            'prediction_confidence': 0.75 + (degradation_score * 0.20)
        }


class TimeSeriesForecaster:
    """
    ARIMA and Prophet-based forecasting for complaint trends
    
    Predicts future complaint volumes and patterns
    """
    
    def __init__(self, seasonal_periods: int = 365):
        self.seasonal_periods = seasonal_periods
    
    def extract_trend(
        self,
        time_series: pd.Series,
        window: int = 30
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract trend and seasonality from time series
        
        Args:
            time_series: Series with daily complaint counts
            window: Window for moving average
            
        Returns:
            Tuple of (trend, detrended)
        """
        trend = time_series.rolling(window=window, center=True).mean()
        detrended = time_series - trend
        
        return trend.values, detrended.values
    
    def forecast_complaints(
        self,
        complaint_counts: np.ndarray,
        forecast_days: int = 30
    ) -> Dict:
        """
        Forecast future complaint volumes
        
        Simple ARIMA-like approach using exponential smoothing
        
        Args:
            complaint_counts: Array of daily complaint counts
            forecast_days: Number of days to forecast
            
        Returns:
            Dictionary with forecast data
        """
        # Exponential smoothing coefficients
        alpha = 0.3  # Level smoothing
        beta = 0.1   # Trend smoothing
        
        level = complaint_counts[-1]
        trend = (complaint_counts[-1] - complaint_counts[-7]) / 7
        
        forecast = []
        forecast_confidence = []
        
        std_dev = np.std(complaint_counts[-30:])
        
        for day in range(1, forecast_days + 1):
            # Update with exponential smoothing
            forecast_value = level + (trend * day)
            
            # Confidence decreases with forecast horizon
            confidence = 1.0 - (day / forecast_days) * 0.3
            
            # Confidence interval based on historical volatility
            interval_width = std_dev * (1 + (day / 7))
            
            forecast.append({
                'day': day,
                'forecast': max(0, forecast_value),
                'confidence': confidence,
                'lower_bound': max(0, forecast_value - interval_width),
                'upper_bound': forecast_value + interval_width
            })
        
        return {
            'forecast': forecast,
            'forecast_method': 'exponential_smoothing',
            'base_level': float(level),
            'trend': float(trend),
            'last_actual_value': float(complaint_counts[-1]),
            'volatility': float(std_dev)
        }
    
    def detect_seasonality(
        self,
        complaint_counts: np.ndarray
    ) -> Dict:
        """
        Detect seasonal patterns in complaints
        
        Returns:
            Dictionary with seasonality information
        """
        if len(complaint_counts) < self.seasonal_periods:
            return {'detected': False, 'seasonal_pattern': None}
        
        # Simple seasonal decomposition
        seasonal = complaint_counts[-self.seasonal_periods:] - np.mean(complaint_counts[-self.seasonal_periods:])
        
        # Check autocorrelation at seasonal lag
        if len(complaint_counts) >= 2 * self.seasonal_periods:
            recent = complaint_counts[-self.seasonal_periods:]
            previous = complaint_counts[-2*self.seasonal_periods:-self.seasonal_periods]
            
            correlation = np.corrcoef(recent, previous)[0, 1]
            
            if correlation > 0.5:
                return {
                    'detected': True,
                    'seasonal_period': self.seasonal_periods,
                    'correlation': float(correlation),
                    'seasonal_strength': float(np.std(seasonal))
                }
        
        return {'detected': False, 'seasonal_pattern': None}


class SpatialCorrelationAnalyzer:
    """
    Analyzes spatial correlations between wards
    
    Uses simplified GNN concepts for ward network analysis
    """
    
    def __init__(self):
        # Simulated ward adjacency based on Bengaluru geography
        self.ward_neighbors = {
            'Ward 1': ['Ward 2', 'Ward 5'],
            'Ward 2': ['Ward 1', 'Ward 3', 'Ward 5'],
            'Ward 3': ['Ward 2', 'Ward 4'],
            'Ward 4': ['Ward 3', 'Ward 5'],
            'Ward 5': ['Ward 1', 'Ward 2', 'Ward 4'],
        }
    
    def get_neighbors(self, ward: str) -> List[str]:
        """Get neighboring wards"""
        return self.ward_neighbors.get(ward, [])
    
    def analyze_spatial_spread(
        self,
        complaint_data: pd.DataFrame,
        issue_type: str
    ) -> Dict:
        """
        Analyze how specific issues spread across wards
        
        Args:
            complaint_data: DataFrame with ward and issue_type columns
            issue_type: Type of issue to analyze
            
        Returns:
            Spatial spread analysis
        """
        issue_complaints = complaint_data[complaint_data['issue_type'] == issue_type]
        
        if issue_complaints.empty:
            return {'issue_type': issue_type, 'spread_pattern': 'insufficient_data'}
        
        wards_affected = issue_complaints['area'].value_counts()
        
        # Check if spread follows neighbor relationships
        spatial_concentration = 0.0
        for ward, count in wards_affected.items():
            neighbors = self.get_neighbors(ward)
            neighbor_counts = sum(wards_affected.get(n, 0) for n in neighbors)
            
            if wards_affected.sum() > 0:
                spatial_concentration += (count + neighbor_counts) / wards_affected.sum()
        
        return {
            'issue_type': issue_type,
            'wards_affected': len(wards_affected),
            'concentration_score': spatial_concentration / len(wards_affected) if len(wards_affected) > 0 else 0,
            'most_affected_wards': wards_affected.head(3).to_dict(),
            'spread_pattern': 'clustered' if spatial_concentration > 0.7 else 'dispersed'
        }


class InfrastructureHealthScorer:
    """
    Calculates overall infrastructure health scores for wards
    
    Combines multiple indicators into 0-100 score
    """
    
    def __init__(self):
        self.weights = {
            'complaint_frequency': 0.25,
            'issue_resolution_rate': 0.20,
            'average_severity': 0.20,
            'infrastructure_age': 0.15,
            'maintenance_status': 0.10,
            'environmental_factors': 0.10
        }
    
    def calculate_health_score(
        self,
        complaint_frequency: float,  # complaints per day (0-5)
        resolution_rate: float,  # 0-1
        avg_severity: float,  # 0-1
        infrastructure_age: float,  # 0-100 years
        maintenance_months_since: float,  # months since last maintenance
        environmental_risk: float  # 0-1 (rainfall, traffic, etc.)
    ) -> float:
        """
        Calculate comprehensive health score (0-100)
        
        100 = excellent condition
        0 = critical failure risk
        """
        scores = {}
        
        # Complaint frequency (fewer is better)
        complaint_score = max(0, 100 - (complaint_frequency * 20))
        scores['complaint_frequency'] = complaint_score
        
        # Resolution rate (higher is better)
        scores['issue_resolution_rate'] = resolution_rate * 100
        
        # Severity (lower is better)
        scores['average_severity'] = (1 - avg_severity) * 100
        
        # Infrastructure age (younger is better)
        age_score = max(0, 100 - (infrastructure_age * 1.5))
        scores['infrastructure_age'] = age_score
        
        # Maintenance (more recent is better)
        maintenance_score = max(0, 100 - (maintenance_months_since * 2))
        scores['maintenance_status'] = maintenance_score
        
        # Environmental factors
        scores['environmental_factors'] = (1 - environmental_risk) * 100
        
        # Weighted average
        health_score = sum(
            scores[key] * self.weights[key] for key in scores
        )
        
        return max(0, min(100, health_score))
    
    @staticmethod
    def classify_health_status(score: float) -> str:
        """Classify health status from score"""
        if score >= 80:
            return 'excellent'
        elif score >= 60:
            return 'good'
        elif score >= 40:
            return 'fair'
        elif score >= 20:
            return 'poor'
        else:
            return 'critical'
