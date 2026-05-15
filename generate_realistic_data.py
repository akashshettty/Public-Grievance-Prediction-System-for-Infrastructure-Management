"""
Realistic Fake Data Generator for UrbanPulse AI
Generates comprehensive test datasets for all API endpoints
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import random
from typing import List, Dict, Any

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Define paths
DATA_DIR = Path(__file__).parent / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Bengaluru wards
WARDS = [
    "Ward 1", "Ward 5", "Ward 10", "Ward 15", "Ward 20",
    "Ward 25", "Ward 30", "Ward 35", "Ward 40", "Ward 45",
    "Ward 50", "Ward 55", "Ward 60", "Ward 65", "Ward 70",
    "Ward 75", "Ward 80", "Ward 84", "Ward 85", "Ward 90",
    "Ward 95", "Ward 100", "Ward 105", "Ward 110", "Ward 115",
    "Ward 120", "Ward 125", "Ward 130", "Ward 135", "Ward 140",
    "Ward 145", "Ward 150 - Bellandur", "Ward 155", "Ward 160", "Ward 165",
    "Ward 170", "Ward 174 - HSR Layout", "Ward 175", "Ward 180", "Ward 185"
]

ISSUE_TYPES = [
    "Pothole", "Drainage Issues", "Water Overflow", "Street Light Out",
    "Garbage Accumulation", "Road Damage", "Waterlogging", "Erosion",
    "Traffic Signal Malfunction", "Encroachment", "Sidewalk Damage",
    "Manhole Damage", "Cable Issues", "Concrete Damage"
]

STATUSES = ["Pending", "In Progress", "Resolved", "Reopened", "Closed"]

PRIORITY_LEVELS = ["Low", "Medium", "High", "Critical"]


def generate_grievances_data(num_records: int = 50000) -> pd.DataFrame:
    """Generate realistic grievance complaint data."""
    data = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        complaint_date = base_date + timedelta(days=random.randint(0, 365))
        resolution_date = complaint_date + timedelta(days=random.randint(1, 60)) if random.random() > 0.2 else None
        
        data.append({
            'complaint_id': f'COMP-2024-{i:06d}',
            'ward': random.choice(WARDS),
            'issue_type': random.choice(ISSUE_TYPES),
            'description': f'Issue report regarding {random.choice(ISSUE_TYPES).lower()} in the ward',
            'complainant_name': f'Citizen_{i}',
            'contact_number': f'98{random.randint(10000000, 99999999)}',
            'complaint_date': complaint_date.strftime('%Y-%m-%d'),
            'complaint_time': f'{random.randint(6, 23):02d}:{random.randint(0, 59):02d}',
            'status': random.choice(STATUSES),
            'resolution_date': resolution_date.strftime('%Y-%m-%d') if resolution_date else None,
            'assigned_to': f'Staff_{random.randint(1, 100)}',
            'priority': random.choice(PRIORITY_LEVELS),
            'severity_score': round(random.uniform(1, 5), 2),
            'days_unresolved': (datetime.now() - complaint_date).days,
            'reopened_count': random.randint(0, 3) if random.random() > 0.7 else 0,
            'citizen_rating': round(random.uniform(1, 5), 1) if resolution_date else None,
            'sentiment': random.choice(['negative', 'neutral', 'positive']),
            'location_lat': round(12.9716 + random.uniform(-0.1, 0.1), 4),
            'location_lon': round(77.5946 + random.uniform(-0.1, 0.1), 4),
            'social_mentions': random.randint(0, 500),
            'news_coverage': random.choice([True, False])
        })
    
    return pd.DataFrame(data)


def generate_risk_scores(grievances_df: pd.DataFrame) -> pd.DataFrame:
    """Generate area risk scores based on grievances."""
    risk_data = []
    
    for ward in grievances_df['ward'].unique():
        ward_complaints = grievances_df[grievances_df['ward'] == ward]
        
        risk_data.append({
            'ward': ward,
            'total_complaints': len(ward_complaints),
            'pending_complaints': len(ward_complaints[ward_complaints['status'] == 'Pending']),
            'avg_severity': ward_complaints['severity_score'].mean(),
            'avg_resolution_days': ward_complaints['days_unresolved'].mean(),
            'reopening_rate': (ward_complaints['reopened_count'].sum() / max(len(ward_complaints), 1)) * 100,
            'citizen_satisfaction': ward_complaints['citizen_rating'].mean() if ward_complaints['citizen_rating'].notna().any() else 3.5,
            'risk_score': round(random.uniform(0.2, 0.95), 3),
            'risk_classification': np.random.choice(['Low', 'Medium', 'High', 'Critical'], p=[0.3, 0.3, 0.25, 0.15]),
            'trend': np.random.choice(['Improving', 'Stable', 'Declining']),
            'infrastructure_health_index': round(random.uniform(30, 95), 2),
            'forecast_next_month': random.randint(5, 100)
        })
    
    return pd.DataFrame(risk_data)


def generate_hotspot_predictions(num_records: int = 1000) -> pd.DataFrame:
    """Generate hotspot prediction data."""
    data = []
    
    for i in range(num_records):
        data.append({
            'hotspot_id': f'HS-2024-{i:05d}',
            'ward': random.choice(WARDS),
            'location_lat': round(12.9716 + random.uniform(-0.1, 0.1), 4),
            'location_lon': round(77.5946 + random.uniform(-0.1, 0.1), 4),
            'issue_type': random.choice(ISSUE_TYPES),
            'prediction_score': round(random.uniform(0.5, 0.99), 3),
            'confidence': round(random.uniform(0.7, 0.99), 3),
            'complaint_density': random.randint(5, 100),
            'predicted_date': (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'severity_estimate': random.choice(PRIORITY_LEVELS),
            'recurring': random.choice([True, False]),
            'estimated_impact': random.randint(50, 1000),
            'model_version': '2.1'
        })
    
    return pd.DataFrame(data)


def generate_area_features(grievances_df: pd.DataFrame) -> pd.DataFrame:
    """Generate area/ward feature engineering data."""
    features_data = []
    
    for ward in grievances_df['ward'].unique():
        ward_complaints = grievances_df[grievances_df['ward'] == ward]
        
        features_data.append({
            'ward': ward,
            'complaint_count_7d': random.randint(0, 20),
            'complaint_count_30d': random.randint(0, 100),
            'complaint_count_90d': random.randint(0, 300),
            'avg_complaint_severity': ward_complaints['severity_score'].mean(),
            'max_complaint_severity': ward_complaints['severity_score'].max(),
            'avg_resolution_time_days': ward_complaints['days_unresolved'].mean(),
            'complaint_variance': ward_complaints['severity_score'].std(),
            'repeat_complainant_ratio': round(random.uniform(0.1, 0.5), 2),
            'infrastructure_age_avg': random.randint(2, 20),
            'population_density': random.randint(1000, 50000),
            'socioeconomic_index': round(random.uniform(0.2, 0.9), 2),
            'seasonal_trend': np.random.choice(['Summer_High', 'Monsoon_High', 'Stable']),
            'road_network_condition': round(random.uniform(0.3, 0.95), 2),
            'drainage_adequacy': round(random.uniform(0.2, 0.9), 2),
            'maintenance_frequency': random.randint(1, 12),
            'last_major_repair_months_ago': random.randint(0, 60)
        })
    
    return pd.DataFrame(features_data)


def generate_infrastructure_intelligence(num_records: int = 30000) -> pd.DataFrame:
    """Generate comprehensive infrastructure intelligence data."""
    data = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        inspection_date = base_date + timedelta(days=random.randint(0, 365))
        
        data.append({
            'infrastructure_id': f'INF-2024-{i:06d}',
            'ward': random.choice(WARDS),
            'type': random.choice(['Road', 'Drain', 'Streetlight', 'Water Supply', 'Sewage']),
            'location_lat': round(12.9716 + random.uniform(-0.1, 0.1), 4),
            'location_lon': round(77.5946 + random.uniform(-0.1, 0.1), 4),
            'condition_status': random.choice(['Good', 'Fair', 'Poor', 'Critical']),
            'age_years': random.randint(0, 30),
            'last_maintenance_date': (inspection_date - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'maintenance_cost_estimate': random.randint(5000, 500000),
            'failure_risk_score': round(random.uniform(0.1, 0.95), 3),
            'inspection_date': inspection_date.strftime('%Y-%m-%d'),
            'inspection_notes': 'Routine inspection completed',
            'predicted_failure_date': (inspection_date + timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d') if random.random() > 0.7 else None,
            'maintenance_priority': random.choice(['Low', 'Medium', 'High', 'Urgent']),
            'estimated_lifespan_remaining_years': random.randint(0, 20),
            'repair_history_count': random.randint(0, 15),
            'material_type': random.choice(['Asphalt', 'Concrete', 'PVC', 'Cast Iron', 'RCC']),
            'length_or_area': round(random.uniform(10, 1000), 2),
            'capacity_utilization': round(random.uniform(0.3, 1.1), 2)
        })
    
    return pd.DataFrame(data)


def generate_hotspot_training_data(num_records: int = 20000) -> pd.DataFrame:
    """Generate historical hotspot training data."""
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(num_records):
        date = base_date + timedelta(days=random.randint(0, 365))
        
        data.append({
            'training_id': f'TRAIN-2023-{i:06d}',
            'ward': random.choice(WARDS),
            'date': date.strftime('%Y-%m-%d'),
            'issue_type': random.choice(ISSUE_TYPES),
            'complaint_count': random.randint(1, 50),
            'severity_avg': round(random.uniform(1, 5), 2),
            'weather': random.choice(['Clear', 'Cloudy', 'Rainy', 'Sunny']),
            'is_hotspot': random.choice([True, False]),
            'location_lat': round(12.9716 + random.uniform(-0.1, 0.1), 4),
            'location_lon': round(77.5946 + random.uniform(-0.1, 0.1), 4),
            'traffic_density': random.randint(0, 10),
            'population_activity': random.choice(['Low', 'Medium', 'High', 'Very High']),
            'maintenance_recent': random.choice([True, False])
        })
    
    return pd.DataFrame(data)


def main():
    """Generate all datasets."""
    print("🔄 Generating realistic fake datasets...")
    
    # Generate grievances
    print("📋 Generating grievance complaints (50,000 records)...")
    grievances_df = generate_grievances_data(50000)
    grievances_df.to_csv(DATA_DIR / "grievances_cleaned.csv", index=False)
    print(f"   ✅ Saved to {DATA_DIR / 'grievances_cleaned.csv'}")
    
    # Generate risk scores
    print("📊 Generating risk scores...")
    risk_df = generate_risk_scores(grievances_df)
    risk_df.to_csv(DATA_DIR / "area_risk_scores.csv", index=False)
    print(f"   ✅ Saved to {DATA_DIR / 'area_risk_scores.csv'}")
    
    # Generate hotspot predictions
    print("🔥 Generating hotspot predictions (1,000 records)...")
    hotspot_df = generate_hotspot_predictions(1000)
    hotspot_df.to_csv(DATA_DIR / "hotspot_predictions.csv", index=False)
    print(f"   ✅ Saved to {DATA_DIR / 'hotspot_predictions.csv'}")
    
    # Generate area features
    print("🏘️ Generating area features...")
    features_df = generate_area_features(grievances_df)
    features_df.to_csv(DATA_DIR / "area_features.csv", index=False)
    print(f"   ✅ Saved to {DATA_DIR / 'area_features.csv'}")
    
    # Generate infrastructure intelligence
    print("🏗️ Generating infrastructure intelligence (30,000 records)...")
    infra_df = generate_infrastructure_intelligence(30000)
    infra_df.to_csv(DATA_DIR / "infrastructure_intelligence_master.csv", index=False)
    print(f"   ✅ Saved to {DATA_DIR / 'infrastructure_intelligence_master.csv'}")
    
    # Generate hotspot training data
    print("📚 Generating hotspot training data (20,000 records)...")
    training_df = generate_hotspot_training_data(20000)
    training_df.to_csv(DATA_DIR / "hotspot_training_data.csv", index=False)
    print(f"   ✅ Saved to {DATA_DIR / 'hotspot_training_data.csv'}")
    
    # Generate bengaluru master (copy of grievances with extra columns)
    print("🗺️ Generating Bengaluru master dataset...")
    master_df = grievances_df.copy()
    master_df['dataset_version'] = '2.0'
    master_df['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    master_df.to_csv(DATA_DIR / "bengaluru_master.csv", index=False)
    print(f"   ✅ Saved to {DATA_DIR / 'bengaluru_master.csv'}")
    
    print("\n✨ Dataset generation complete!")
    print(f"📁 All files saved to: {DATA_DIR}")
    print(f"\nTotal records generated:")
    print(f"   - Grievances: {len(grievances_df):,}")
    print(f"   - Risk Scores: {len(risk_df):,}")
    print(f"   - Hotspot Predictions: {len(hotspot_df):,}")
    print(f"   - Area Features: {len(features_df):,}")
    print(f"   - Infrastructure Intelligence: {len(infra_df):,}")
    print(f"   - Hotspot Training Data: {len(training_df):,}")
    print(f"\n💾 Total data: {(50000 + len(risk_df) + 1000 + len(features_df) + 30000 + 20000):,} records")


if __name__ == "__main__":
    main()
