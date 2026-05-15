#!/usr/bin/env python3
"""Test script to verify data loading."""

from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, '/f/urbanpluse2')

from backend.services.data_service import DataService
from backend.config import get_config

config = get_config()

print("Testing data loading...")
print(f"Data path: {config.PROCESSED_DATA_DIR}")

# Test loading grievances
print("\n1. Loading grievances data...")
service = DataService()
grievances = service.get_grievances_data()
print(f"   ✅ Loaded {len(grievances)} grievance records")
print(f"   Columns: {list(grievances.columns)[:5]}...")

# Test loading risk data
print("\n2. Loading risk scores data...")
risk = service.get_risk_data()
print(f"   ✅ Loaded {len(risk)} risk records")
print(f"   Columns: {list(risk.columns)[:5]}...")

# Test basic filtering
print("\n3. Testing data filtering...")
grievances['days_unresolved'] = (pd.Timestamp.now() - pd.to_datetime(grievances['complaint_date'])).dt.days
high_risk = grievances[
    (grievances['days_unresolved'] > 10) | 
    (grievances['severity_score'] > 4) |
    (grievances['reopened_count'] > 0)
].head(5)
print(f"   ✅ Found {len(high_risk)} high-risk complaints")

if len(high_risk) > 0:
    print(f"   First record:")
    print(f"     - complaint_id: {high_risk.iloc[0]['complaint_id']}")
    print(f"     - ward: {high_risk.iloc[0]['ward']}")
    print(f"     - severity: {high_risk.iloc[0]['severity_score']}")

print("\n✨ Data loading test passed!")
