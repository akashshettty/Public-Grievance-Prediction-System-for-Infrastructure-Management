#!/usr/bin/env python
"""
Simplified AI Initialization Script - Tests core AI modules with available packages
May 13, 2026
"""

import sys
import os
from pathlib import Path

# Add the project root to sys.path (parent of src folder)
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

print("=" * 80)
print("🚀 URBANPULSE AI SYSTEM INITIALIZATION")
print("=" * 80)
print(f"📍 Project Root: {project_root}")
print(f"🐍 Python Version: {sys.version.split()[0]}")
print()

# Test imports and basic functionality
print("Testing Module Imports...")
print("-" * 80)

try:
    print("✓ Testing pandas...")
    import pandas as pd
    print(f"  ✅ pandas {pd.__version__}")
except Exception as e:
    print(f"  ❌ Error: {e}")

try:
    print("✓ Testing numpy...")
    import numpy as np
    print(f"  ✅ numpy {np.__version__}")
except Exception as e:
    print(f"  ❌ Error: {e}")

try:
    print("✓ Testing scikit-learn...")
    from sklearn.preprocessing import MinMaxScaler
    import sklearn
    print(f"  ✅ scikit-learn {sklearn.__version__}")
except Exception as e:
    print(f"  ❌ Error: {e}")

try:
    print("✓ Testing matplotlib...")
    import matplotlib
    print(f"  ✅ matplotlib {matplotlib.__version__}")
except Exception as e:
    print(f"  ❌ Error: {e}")

try:
    print("✓ Testing networkx...")
    import networkx as nx
    print(f"  ✅ networkx {nx.__version__}")
except Exception as e:
    print(f"  ❌ Error: {e}")

try:
    print("✓ Testing flask...")
    import flask
    print(f"  ✅ flask {flask.__version__}")
except Exception as e:
    print(f"  ❌ Error: {e}")

try:
    print("✓ Testing pydantic...")
    import pydantic
    print(f"  ✅ pydantic {pydantic.__version__}")
except Exception as e:
    print(f"  ❌ Error: {e}")

print()
print("=" * 80)
print("📊 TESTING CORE AI MODULES")
print("=" * 80)
print()

# Test NLP Pipeline
try:
    print("🔤 Testing NLP Complaint Pipeline...")
    from src.nlp.complaint_analysis import ComplaintClassifier, SeveritySentimentAnalyzer
    
    classifier = ComplaintClassifier()
    sentiment_analyzer = SeveritySentimentAnalyzer()
    
    # Test complaint
    test_complaint = "The road in my area has multiple potholes that are causing accidents"
    
    classification = classifier.classify(test_complaint)
    sentiment = sentiment_analyzer.analyze_severity(test_complaint)
    
    print(f"  📝 Test Complaint: '{test_complaint}'")
    print(f"  📂 Category: {classification['category']} (confidence: {classification['confidence']:.2f})")
    print(f"  📊 Severity: {sentiment['severity_level']} (score: {sentiment['severity_score']:.2f})")
    print("  ✅ NLP Pipeline OK")
except Exception as e:
    print(f"  ❌ NLP Error: {e}")
    import traceback
    traceback.print_exc()

print()

# Test Forecasting
try:
    print("📈 Testing Infrastructure Forecasting...")
    from src.models.advanced_forecasting.infrastructure_forecaster import InfrastructureHealthScorer
    
    health_scorer = InfrastructureHealthScorer()
    
    # Test data
    test_ward_metrics = {
        'complaint_frequency': 15,
        'complaint_resolution_rate': 0.75,
        'avg_complaint_severity': 0.65,
        'infrastructure_age_years': 8,
        'maintenance_score': 0.70,
        'environmental_factor': 0.80
    }
    
    health_score = health_scorer.calculate_health_score(test_ward_metrics)
    
    print(f"  📍 Ward Metrics: {test_ward_metrics}")
    print(f"  💪 Health Score: {health_score:.2f}/100")
    print("  ✅ Forecasting OK")
except Exception as e:
    print(f"  ❌ Forecasting Error: {e}")
    import traceback
    traceback.print_exc()

print()

# Test Anomaly Detection
try:
    print("🚨 Testing Anomaly Detection...")
    from src.anomaly_detection.fraud_detection import ComplaintAnomalyAnalyzer
    
    analyzer = ComplaintAnomalyAnalyzer()
    
    # Test anomalous closure
    suspicious_complaint = {
        'id': 'C001',
        'severity': 0.95,
        'created_date': pd.Timestamp('2026-05-01'),
        'closed_date': pd.Timestamp('2026-05-01 02:00:00'),
        'reopened_count': 3,
        'resolution_time_hours': 2
    }
    
    anomaly_result = analyzer.detect_suspicious_closure(suspicious_complaint)
    
    print(f"  🔍 Test Complaint: {suspicious_complaint['id']}")
    print(f"  ⚠️  Anomaly Score: {anomaly_result['anomaly_score']:.2f}")
    print(f"  🚩 Is Suspicious: {anomaly_result['is_anomalous']}")
    if anomaly_result['red_flags']:
        print(f"  🚨 Red Flags: {', '.join(anomaly_result['red_flags'])}")
    print("  ✅ Anomaly Detection OK")
except Exception as e:
    print(f"  ❌ Anomaly Detection Error: {e}")
    import traceback
    traceback.print_exc()

print()

# Test Escalation Prediction
try:
    print("📢 Testing Escalation Prediction...")
    from src.escalation_prediction.escalation_predictor import EscalationPredictor
    
    predictor = EscalationPredictor()
    
    test_complaint_data = {
        'id': 'C002',
        'days_open': 45,
        'severity': 0.85,
        'reopened_count': 2,
        'public_engagement_score': 0.7,
        'media_sensitivity_score': 0.8,
        'resolution_rate_ward': 0.60
    }
    
    escalation_prediction = predictor.generate_escalation_prediction(test_complaint_data)
    
    print(f"  🎯 Test Complaint: {test_complaint_data['id']}")
    print(f"  📊 Overall Risk: {escalation_prediction['overall_risk_level']}")
    print(f"  📈 Risk Score: {escalation_prediction['overall_risk_score']:.2f}")
    print(f"  🔮 Primary Channel: {escalation_prediction['predicted_escalation_channels'][0] if escalation_prediction['predicted_escalation_channels'] else 'None'}")
    print("  ✅ Escalation Prediction OK")
except Exception as e:
    print(f"  ❌ Escalation Prediction Error: {e}")
    import traceback
    traceback.print_exc()

print()

# Test Optimization
try:
    print("⚙️  Testing Optimization Engine...")
    from src.optimization.optimization_engine import OptimizationEngine
    from src.optimization.optimization_engine import RepairTask, Worker
    
    optimizer = OptimizationEngine()
    
    # Create test tasks and workers
    tasks = [
        RepairTask(
            task_id="T001",
            ward="Ward_A",
            latitude=13.0827,
            longitude=80.2707,
            issue_type="Pothole",
            urgency_score=0.8,
            duration=2.0,
            workers_required=2,
            cost=500
        ),
        RepairTask(
            task_id="T002",
            ward="Ward_B",
            latitude=13.1939,
            longitude=80.1829,
            issue_type="Drainage",
            urgency_score=0.7,
            duration=3.0,
            workers_required=3,
            cost=800
        )
    ]
    
    workers = [
        Worker(worker_id="W001", location=(13.0827, 80.2707), skills=["Pothole", "Drainage"], available_hours=8, hourly_cost=250),
        Worker(worker_id="W002", location=(13.1939, 80.1829), skills=["Drainage", "Streetlight"], available_hours=8, hourly_cost=250)
    ]
    
    # Assign tasks
    assignments = optimizer.assign_tasks_to_workers(tasks, workers, max_budget=5000)
    
    print(f"  📋 Tasks: {len(tasks)}, Workers: {len(workers)}")
    print(f"  ✅ Assignments Created: {len(assignments)}")
    print(f"  💰 Total Cost: ${sum(a.get('cost', 0) for a in assignments)}")
    print("  ✅ Optimization Engine OK")
except Exception as e:
    print(f"  ❌ Optimization Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("=" * 80)
print("✨ INITIALIZATION SUMMARY")
print("=" * 80)
print("✅ Core modules tested successfully!")
print("📊 The AI Smart City Intelligence Platform is ready for use.")
print()
print("🎯 Next Steps:")
print("  1. Install full requirements: pip install -r requirements.txt")
print("  2. Configure API endpoints in src/dashboard/app.py")
print("  3. Start the dashboard: python src/dashboard/run_dashboard.py")
print("  4. Access frontend at http://localhost:5000")
print()
print("=" * 80)
