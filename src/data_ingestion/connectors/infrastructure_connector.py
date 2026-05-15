"""
Infrastructure Data Connectors
Population density, road age, repair history
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from pathlib import Path


class PopulationDensityConnector:
    """Provides population density data for wards"""
    
    def __init__(self):
        # Simulated ward-level population density data (based on Bengaluru census)
        self.ward_population_data = {
            'Ward 1': {'population': 185000, 'area_sqkm': 12.5, 'density_per_sqkm': 14800},
            'Ward 2': {'population': 210000, 'area_sqkm': 14.2, 'density_per_sqkm': 14789},
            'Ward 3': {'population': 195000, 'area_sqkm': 11.8, 'density_per_sqkm': 16525},
            'Ward 4': {'population': 165000, 'area_sqkm': 15.3, 'density_per_sqkm': 10784},
            'Ward 5': {'population': 225000, 'area_sqkm': 9.5, 'density_per_sqkm': 23684},
        }
    
    def get_population_density_data(self, ward_list: List[str]) -> pd.DataFrame:
        """
        Get population density data for wards
        
        Args:
            ward_list: List of ward names
            
        Returns:
            DataFrame with population metrics
        """
        records = []
        for ward in ward_list:
            if ward in self.ward_population_data:
                data = self.ward_population_data[ward]
                records.append({
                    'ward': ward,
                    'population': data['population'],
                    'area_sqkm': data['area_sqkm'],
                    'density_per_sqkm': data['density_per_sqkm'],
                    'is_high_density': data['density_per_sqkm'] > 15000
                })
            else:
                # Generate reasonable estimates for unknown wards
                records.append({
                    'ward': ward,
                    'population': np.random.normal(190000, 20000),
                    'area_sqkm': np.random.normal(12, 3),
                    'density_per_sqkm': np.random.normal(15000, 3000),
                    'is_high_density': np.random.random() > 0.5
                })
        
        return pd.DataFrame(records)


class RoadAgeConnector:
    """Provides road age and infrastructure degradation data"""
    
    def __init__(self):
        self.current_year = 2024
    
    def generate_road_age_data(self, ward_list: List[str]) -> pd.DataFrame:
        """
        Generate road age data for wards
        
        Older roads are more prone to damage (potholes, drainage issues)
        """
        np.random.seed(42)
        road_records = []
        
        for ward in ward_list:
            # Each ward has multiple road segments
            num_segments = np.random.randint(5, 15)
            
            for segment_id in range(num_segments):
                # Road construction year varies
                construction_year = np.random.randint(1980, 2020)
                road_age = self.current_year - construction_year
                
                # Quality degrades with age
                base_quality = 100 - (road_age * 2)
                quality_score = max(10, min(100, base_quality + np.random.normal(0, 10)))
                
                # Maintenance frequency decreases quality if not done
                last_major_repair = self.current_year - np.random.randint(1, 10)
                years_since_repair = self.current_year - last_major_repair
                
                # Infrastructure characteristics
                has_drainage = np.random.random() > 0.3
                is_arterial_road = np.random.random() > 0.7
                
                road_records.append({
                    'ward': ward,
                    'road_segment_id': f"{ward}_road_{segment_id}",
                    'construction_year': construction_year,
                    'road_age_years': road_age,
                    'current_quality_score': quality_score,
                    'last_major_repair_year': last_major_repair,
                    'years_since_repair': years_since_repair,
                    'has_drainage_system': has_drainage,
                    'is_arterial_road': is_arterial_road,
                    'estimated_remaining_life_years': max(1, 50 - road_age),
                    'maintenance_urgency': self._classify_urgency(road_age, years_since_repair)
                })
        
        return pd.DataFrame(road_records)
    
    @staticmethod
    def _classify_urgency(road_age: int, years_since_repair: int) -> str:
        """Classify maintenance urgency"""
        if road_age > 40 or years_since_repair > 5:
            return 'critical'
        elif road_age > 25 or years_since_repair > 3:
            return 'high'
        elif road_age > 15 or years_since_repair > 2:
            return 'medium'
        else:
            return 'low'
    
    def aggregate_by_ward(self, road_data: pd.DataFrame) -> pd.DataFrame:
        """Aggregate road data to ward level"""
        return road_data.groupby('ward').agg({
            'road_age_years': 'mean',
            'current_quality_score': 'mean',
            'years_since_repair': 'mean',
            'has_drainage_system': 'mean',
            'is_arterial_road': 'mean',
            'estimated_remaining_life_years': 'mean',
            'road_segment_id': 'count'
        }).rename(columns={'road_segment_id': 'num_road_segments'}).reset_index()


class RepairHistoryConnector:
    """Provides historical repair and maintenance data"""
    
    def __init__(self):
        self.current_date = pd.Timestamp.now()
    
    def generate_repair_history(self, ward_list: List[str], num_months: int = 24) -> pd.DataFrame:
        """
        Generate repair history for wards
        
        Args:
            ward_list: List of ward names
            num_months: Number of months of history to generate
            
        Returns:
            DataFrame with repair records
        """
        np.random.seed(42)
        repair_records = []
        
        start_date = self.current_date - pd.DateOffset(months=num_months)
        dates = pd.date_range(start=start_date, end=self.current_date, freq='D')
        
        for ward in ward_list:
            # Different wards have different repair frequencies
            num_repairs = np.random.randint(5, 20)
            repair_dates = np.random.choice(dates, size=num_repairs, replace=False)
            
            for repair_date in repair_dates:
                issue_types = ['Pothole', 'Drainage blockage', 'Road crack', 'Pavement damage', 'Manhole issue']
                
                repair_records.append({
                    'ward': ward,
                    'repair_date': repair_date,
                    'issue_type': np.random.choice(issue_types),
                    'repair_cost_estimate': np.random.uniform(5000, 50000),
                    'repair_duration_days': np.random.randint(1, 15),
                    'completion_status': np.random.choice(['completed', 'delayed', 'incomplete'], p=[0.7, 0.2, 0.1]),
                    'worker_team_size': np.random.randint(2, 8),
                    'material_used': ['concrete', 'asphalt', 'bitumen'][np.random.randint(0, 3)]
                })
        
        df = pd.DataFrame(repair_records)
        df['repair_date'] = pd.to_datetime(df['repair_date'])
        return df
    
    def calculate_repair_metrics(self, repair_history: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate repair metrics by ward
        
        Metrics:
        - Average time to completion
        - Cost efficiency
        - Recurring issue frequency
        """
        metrics = repair_history.groupby('ward').agg({
            'repair_date': 'count',
            'repair_duration_days': 'mean',
            'repair_cost_estimate': ['mean', 'sum'],
            'completion_status': lambda x: (x == 'completed').sum() / len(x)
        }).reset_index()
        
        metrics.columns = ['ward', 'num_repairs', 'avg_duration_days', 
                           'avg_repair_cost', 'total_repair_cost', 'completion_rate']
        
        return metrics
