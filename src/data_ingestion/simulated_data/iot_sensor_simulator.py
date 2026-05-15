"""
Simulated IoT Sensor Feeds for UrbanPulse AI
Generates realistic sensor data for infrastructure monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional
from enum import Enum


class SensorType(Enum):
    """Types of IoT sensors"""
    MOISTURE_SENSOR = "moisture"
    VIBRATION_SENSOR = "vibration"
    PRESSURE_SENSOR = "pressure"
    TEMPERATURE_SENSOR = "temperature"
    FILL_LEVEL_SENSOR = "fill_level"


class IoTSensorSimulator:
    """Simulates IoT sensor networks for smart city infrastructure"""
    
    def __init__(self):
        self.current_date = datetime.now()
    
    def generate_drainage_sensors(
        self,
        ward_list: List[str],
        num_days: int = 90,
        readings_per_day: int = 24
    ) -> pd.DataFrame:
        """
        Generate drainage system sensor data
        
        Monitors:
        - Water level/fill percentage
        - Blockage indicators
        - Flow rate
        - Overflow risk
        """
        np.random.seed(42)
        sensor_records = []
        
        dates = pd.date_range(
            start=self.current_date - timedelta(days=num_days),
            end=self.current_date,
            freq=f'{24//readings_per_day}H'
        )
        
        for ward in ward_list:
            # 2-4 drainage monitoring points per ward
            num_sensors = np.random.randint(2, 5)
            
            for sensor_id in range(num_sensors):
                for date in dates:
                    # Simulate daily patterns
                    hour = date.hour
                    
                    # Higher water levels during morning/afternoon
                    if hour in [6, 7, 8, 9, 10, 11]:
                        base_level = 65
                    elif hour in [12, 13, 14, 15, 16, 17]:
                        base_level = 70
                    elif hour in [18, 19, 20, 21, 22]:
                        base_level = 60
                    else:
                        base_level = 45
                    
                    # Random variation
                    fill_level = base_level + np.random.normal(0, 10)
                    fill_level = max(5, min(100, fill_level))
                    
                    # Overflow risk increases with high fill levels
                    overflow_risk = max(0, min(1, (fill_level - 80) / 20))
                    
                    # Blockage indicators (more likely when levels are high)
                    blockage_score = (fill_level / 100) * 0.7 + np.random.uniform(0, 0.3)
                    
                    sensor_records.append({
                        'timestamp': date,
                        'ward': ward,
                        'sensor_id': f"{ward}_drainage_{sensor_id}",
                        'sensor_type': 'drainage_monitoring',
                        'fill_level_percent': fill_level,
                        'blockage_indicator': blockage_score,
                        'overflow_risk_score': overflow_risk,
                        'flow_rate_lpm': max(0, 100 - fill_level) * np.random.uniform(0.8, 1.2),
                        'requires_attention': fill_level > 85 or blockage_score > 0.7
                    })
        
        return pd.DataFrame(sensor_records)
    
    def generate_road_condition_sensors(
        self,
        ward_list: List[str],
        num_days: int = 90
    ) -> pd.DataFrame:
        """
        Generate road condition sensors
        
        Monitors:
        - Pothole detection (vibration/accelerometer)
        - Surface moisture
        - Temperature
        - Load bearing
        """
        np.random.seed(42)
        sensor_records = []
        
        dates = pd.date_range(
            start=self.current_date - timedelta(days=num_days),
            end=self.current_date,
            freq='D'
        )
        
        for ward in ward_list:
            num_sensors = np.random.randint(3, 7)
            
            for sensor_id in range(num_sensors):
                for date in dates:
                    # Pothole damage index increases with moisture and vehicle load
                    moisture = np.random.uniform(20, 80)
                    
                    # Simulate seasonal patterns
                    month = date.month
                    if month in [6, 7, 8, 9]:  # Monsoon
                        moisture += 30
                    
                    moisture = min(100, moisture)
                    
                    # Pothole risk increases with moisture and age
                    pothole_risk = (moisture / 100) * 0.6 + np.random.uniform(0, 0.4)
                    
                    # Surface deformation indicators
                    vibration_level = pothole_risk * 100 + np.random.uniform(-10, 10)
                    
                    sensor_records.append({
                        'timestamp': date,
                        'ward': ward,
                        'sensor_id': f"{ward}_road_{sensor_id}",
                        'sensor_type': 'road_condition',
                        'surface_moisture_percent': moisture,
                        'vibration_level_units': max(0, vibration_level),
                        'pothole_risk_score': max(0, min(1, pothole_risk)),
                        'temperature_celsius': 25 + np.random.normal(0, 5),
                        'surface_condition': self._classify_surface(pothole_risk),
                        'requires_attention': pothole_risk > 0.6
                    })
        
        return pd.DataFrame(sensor_records)
    
    def generate_water_supply_sensors(
        self,
        ward_list: List[str],
        num_days: int = 90
    ) -> pd.DataFrame:
        """
        Generate water supply infrastructure sensors
        
        Monitors:
        - Pipe pressure
        - Flow rate
        - Leakage detection
        - Water quality
        """
        np.random.seed(42)
        sensor_records = []
        
        dates = pd.date_range(
            start=self.current_date - timedelta(days=num_days),
            end=self.current_date,
            freq='D'
        )
        
        for ward in ward_list:
            num_sensors = np.random.randint(2, 4)
            
            for sensor_id in range(num_sensors):
                for date in dates:
                    # Pressure variations (higher during night, lower during peak usage)
                    hour = date.hour
                    
                    if hour in [22, 23, 0, 1, 2, 3]:
                        base_pressure = 4.5
                    elif hour in [8, 9, 17, 18]:
                        base_pressure = 2.5
                    else:
                        base_pressure = 3.5
                    
                    pressure = base_pressure + np.random.normal(0, 0.3)
                    pressure = max(1, pressure)
                    
                    # Flow rate
                    flow_rate = 50 + np.random.normal(0, 10)
                    
                    # Leakage detection (increases with pressure variations and age)
                    pressure_variance = abs(pressure - base_pressure)
                    leakage_risk = (pressure_variance / 2) + np.random.uniform(0, 0.3)
                    leakage_risk = min(1, leakage_risk)
                    
                    sensor_records.append({
                        'timestamp': date,
                        'ward': ward,
                        'sensor_id': f"{ward}_water_{sensor_id}",
                        'sensor_type': 'water_supply',
                        'pipe_pressure_bar': pressure,
                        'flow_rate_lpm': flow_rate,
                        'leakage_risk_score': leakage_risk,
                        'water_quality_tds': 200 + np.random.normal(0, 30),
                        'requires_attention': leakage_risk > 0.7 or pressure < 1.5
                    })
        
        return pd.DataFrame(sensor_records)
    
    @staticmethod
    def _classify_surface(pothole_risk: float) -> str:
        """Classify surface condition"""
        if pothole_risk < 0.3:
            return 'excellent'
        elif pothole_risk < 0.5:
            return 'good'
        elif pothole_risk < 0.7:
            return 'fair'
        elif pothole_risk < 0.85:
            return 'poor'
        else:
            return 'critical'
    
    def generate_all_sensors(
        self,
        ward_list: List[str],
        num_days: int = 90
    ) -> pd.DataFrame:
        """Generate all sensor types and combine"""
        
        drainage = self.generate_drainage_sensors(ward_list, num_days)
        road = self.generate_road_condition_sensors(ward_list, num_days)
        water = self.generate_water_supply_sensors(ward_list, num_days)
        
        return pd.concat([drainage, road, water], ignore_index=True)
