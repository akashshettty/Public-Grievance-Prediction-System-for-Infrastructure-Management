"""
Initialize and run AI Intelligence pipelines
Main entry point for starting all AI services
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # Go up one level from src/
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.nlp.run_nlp_pipeline import NLPComplaintPipeline
from src.models.advanced_forecasting.infrastructure_forecaster import (
    InfrastructureDegradationPredictor,
    TimeSeriesForecaster,
    InfrastructureHealthScorer
)
from src.optimization.optimization_engine import OptimizationEngine
from src.anomaly_detection.fraud_detection import ComplaintAnomalyAnalyzer
from src.escalation_prediction.escalation_predictor import EscalationPredictor
from src.data_ingestion.connectors.weather_connector import WeatherConnector
from src.data_ingestion.connectors.traffic_connector import TrafficConnector
from src.data_ingestion.connectors.infrastructure_connector import (
    PopulationDensityConnector,
    RoadAgeConnector,
    RepairHistoryConnector
)
from src.data_ingestion.simulated_data.iot_sensor_simulator import IoTSensorSimulator


def initialize_data_sources():
    """Initialize all data ingestion sources"""
    print("\n" + "="*60)
    print("INITIALIZING DATA SOURCES")
    print("="*60)
    
    data_dir = PROJECT_ROOT / "data" / "raw"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Weather data
    print("\n📊 Generating Weather Data...")
    weather_connector = WeatherConnector()
    weather_data = weather_connector.generate_simulated_weather_data(
        start_date=datetime.now() - timedelta(days=365),
        end_date=datetime.now(),
        ward_list=["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"]
    )
    weather_connector.cache_weather_data(weather_data, "bengaluru_weather_2024")
    print(f"   ✓ Generated {len(weather_data)} weather records")
    
    # Traffic data
    print("\n📊 Generating Traffic Data...")
    traffic_connector = TrafficConnector()
    traffic_data = traffic_connector.generate_simulated_traffic_data(
        start_date=datetime.now() - timedelta(days=365),
        end_date=datetime.now(),
        ward_list=["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"]
    )
    traffic_connector.cache_traffic_data(traffic_data, "bengaluru_traffic_2024")
    print(f"   ✓ Generated {len(traffic_data)} traffic records")
    
    # Population & Infrastructure
    print("\n📊 Generating Infrastructure Data...")
    pop_connector = PopulationDensityConnector()
    pop_data = pop_connector.get_population_density_data(["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"])
    print(f"   ✓ Generated population density for {len(pop_data)} wards")
    
    road_connector = RoadAgeConnector()
    road_data = road_connector.generate_road_age_data(["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"])
    print(f"   ✓ Generated road age data for {len(road_data)} segments")
    
    # IoT Sensors
    print("\n📊 Generating IoT Sensor Data...")
    iot_sim = IoTSensorSimulator()
    sensor_data = iot_sim.generate_all_sensors(
        ward_list=["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5"],
        num_days=90
    )
    print(f"   ✓ Generated {len(sensor_data)} sensor readings")
    
    return {
        'weather': weather_data,
        'traffic': traffic_data,
        'population': pop_data,
        'roads': road_data,
        'sensors': sensor_data
    }


def test_nlp_pipeline(complaints_df=None):
    """Test NLP intelligence pipeline"""
    print("\n" + "="*60)
    print("TESTING NLP INTELLIGENCE PIPELINE")
    print("="*60)
    
    if complaints_df is None:
        # Create sample complaints
        complaints_df = pd.DataFrame({
            'complaint_id': ['COMP-001', 'COMP-002', 'COMP-003'],
            'description': [
                'Large pothole near my apartment completely damaged',
                'Drainage blocked for 3 days causing water logging',
                'asdfghjkl qwerty test xyz invalid complaint'
            ],
            'timestamp': [datetime.now() - timedelta(days=i) for i in range(3)]
        })
    
    pipeline = NLPComplaintPipeline()
    
    print("\n🧠 Processing sample complaints...")
    results = pipeline.process_batch(complaints_df)
    
    print("\n📊 NLP Analysis Results:")
    print("-" * 60)
    for idx, row in results.iterrows():
        print(f"\nComplaint: {row['complaint_id']}")
        print(f"  Classification: {row['classification']} ({row['classification_confidence']:.1%})")
        print(f"  Severity: {row['severity_score']:.2f} | Urgency: {row['urgency_score']:.2f}")
        print(f"  Sentiment: {row['sentiment']} ({row['sentiment_score']:.2f})")
        print(f"  Is Fraudulent: {row['is_fraudulent']} (score: {row['fraud_score']:.2f})")
        print(f"  Is Duplicate: {row['is_duplicate']} (similarity: {row['duplicate_similarity']:.2f})")
        print(f"  ✓ {row['recommended_action']}")
    
    return results


def test_forecasting_pipeline():
    """Test infrastructure forecasting pipeline"""
    print("\n" + "="*60)
    print("TESTING FORECASTING PIPELINE")
    print("="*60)
    
    predictor = InfrastructureDegradationPredictor()
    health_scorer = InfrastructureHealthScorer()
    forecaster = TimeSeriesForecaster()
    
    print("\n🔮 Testing Infrastructure Health Scoring...")
    
    ward_analytics = {
        'complaint_count_7d': 12,
        'complaint_count_30d': 45,
        'avg_complaint_age_days': 18,
        'infrastructure_age': 35,
        'days_since_last_repair': 120,
        'avg_rainfall_7d': 15,
        'traffic_density': 72
    }
    
    prediction = predictor.predict_ward_failure_probability(ward_analytics)
    
    health_score = health_scorer.calculate_health_score(
        complaint_frequency=ward_analytics['complaint_count_7d'] / 7,
        resolution_rate=0.80,
        avg_severity=0.58,
        infrastructure_age=ward_analytics['infrastructure_age'],
        maintenance_months_since=ward_analytics['days_since_last_repair'] / 30,
        environmental_risk=ward_analytics['avg_rainfall_7d'] / 50
    )
    
    print(f"\n📊 Ward 5 Health Score: {health_score:.1f}/100")
    print(f"   Status: {health_scorer.classify_health_status(health_score).upper()}")
    print(f"\n⚠️ Degradation Score: {prediction['degradation_score']:.2f}")
    print(f"   Risk Level: {prediction['risk_level'].upper()}")
    print(f"   Failure Probability: {prediction['failure_probability']:.1%}")
    print(f"   Confidence: {prediction['prediction_confidence']:.1%}")
    
    # Test forecasting
    print("\n🔮 Testing Complaint Volume Forecasting...")
    historical_complaints = np.random.randint(5, 25, size=365)
    forecast = forecaster.forecast_complaints(historical_complaints, forecast_days=30)
    
    print(f"\n📈 30-Day Forecast:")
    print(f"   Base Level: {forecast['base_level']:.1f} complaints/day")
    print(f"   Trend: {forecast['trend']:.2f} (linear)")
    print(f"   Volatility: {forecast['volatility']:.2f}")
    print(f"   Method: {forecast['forecast_method']}")


def test_anomaly_detection():
    """Test anomaly and fraud detection"""
    print("\n" + "="*60)
    print("TESTING ANOMALY & FRAUD DETECTION")
    print("="*60)
    
    analyzer = ComplaintAnomalyAnalyzer()
    
    print("\n🔍 Testing Suspicious Closure Detection...")
    
    test_cases = [
        {
            'complaint_id': 'COMP-NORMAL',
            'closure_time_hours': 72,
            'median_closure_time': 100,
            'reopening_count': 0,
            'avg_reopening_count': 0.5,
            'severity_score': 0.5,
            'complaint_age_days': 5,
            'expected': 'Normal'
        },
        {
            'complaint_id': 'COMP-SUSPICIOUS',
            'closure_time_hours': 2,
            'median_closure_time': 100,
            'reopening_count': 0,
            'avg_reopening_count': 0.5,
            'severity_score': 0.85,
            'complaint_age_days': 5,
            'expected': 'Suspicious'
        }
    ]
    
    for test_case in test_cases:
        complaint_id = test_case.pop('complaint_id')
        expected = test_case.pop('expected')
        
        result = analyzer.analyze_complaint_closure(complaint_id, test_case)
        
        print(f"\n{complaint_id}:")
        print(f"   Anomaly Score: {result.anomaly_score:.2f}")
        print(f"   Status: {'⚠️ ANOMALOUS' if result.is_anomalous else '✓ Normal'}")
        print(f"   Type: {result.anomaly_type}")
        print(f"   Expected: {expected}")


def test_escalation_prediction():
    """Test escalation prediction"""
    print("\n" + "="*60)
    print("TESTING ESCALATION PREDICTION")
    print("="*60)
    
    predictor = EscalationPredictor()
    
    print("\n🚨 Testing Escalation Risk Prediction...")
    
    metrics = {
        'complaint_age_days': 45,
        'severity_score': 0.82,
        'reopening_count': 2,
        'description': 'Water contamination in Ward 5 affecting thousands',
        'views_count': 250,
        'resolution_rate_percent': 60,
        'geographic_concentration': 0.8
    }
    
    prediction = predictor.generate_escalation_prediction('COMP-HIGH-RISK', metrics)
    
    print(f"\n📊 Escalation Analysis for {prediction.complaint_id}:")
    print(f"   Risk Score: {prediction.escalation_risk_score:.2f}")
    print(f"   Risk Level: {prediction.risk_level.upper()}")
    print(f"   Probability: {prediction.escalation_probability:.1%}")
    print(f"   Days to Escalation: {prediction.predicted_escalation_time_days}")
    print(f"\n   Escalation Channels:")
    for channel in prediction.likely_escalation_channels:
        print(f"   - {channel}")
    print(f"\n   Mitigation Actions:")
    for idx, action in enumerate(prediction.mitigation_actions, 1):
        print(f"   {idx}. {action}")


def main():
    """Run all initialization and tests"""
    print("\n" + "="*70)
    print(" AI-DRIVEN INFRASTRUCTURE GRIEVANCE INTELLIGENCE SYSTEM")
    print(" Initialization & Testing Suite")
    print("="*70)
    
    try:
        # Initialize data sources
        data_sources = initialize_data_sources()
        
        # Test each pipeline
        test_nlp_pipeline()
        test_forecasting_pipeline()
        test_anomaly_detection()
        test_escalation_prediction()
        
        print("\n" + "="*70)
        print("✅ ALL SYSTEMS INITIALIZED AND TESTED SUCCESSFULLY")
        print("="*70)
        print("\n🚀 Next Steps:")
        print("   1. Start Flask API: python src/dashboard/run_dashboard.py")
        print("   2. Start React frontend: cd frontend && npm run dev")
        print("   3. Access dashboard: http://localhost:3000")
        print("\n📚 Documentation: See UPGRADE_GUIDE.md for complete details")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
