"""
Extended AI Intelligence API Endpoints
Integrates NLP, forecasting, optimization, and anomaly detection
"""

from flask import Flask, jsonify, request
from pathlib import Path
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import AI modules
from src.nlp.run_nlp_pipeline import NLPComplaintPipeline
from src.models.advanced_forecasting.infrastructure_forecaster import (
    InfrastructureDegradationPredictor,
    TimeSeriesForecaster,
    InfrastructureHealthScorer
)
from src.optimization.optimization_engine import OptimizationEngine, RoutingOptimizer
from src.anomaly_detection.fraud_detection import ComplaintAnomalyAnalyzer
from src.escalation_prediction.escalation_predictor import EscalationPredictor


def create_intelligence_api(app: Flask, data_path: Path):
    """
    Create AI intelligence API endpoints
    
    Args:
        app: Flask app instance
        data_path: Path to data directory
    """
    
    # Initialize AI modules
    nlp_pipeline = NLPComplaintPipeline()
    degradation_predictor = InfrastructureDegradationPredictor()
    forecaster = TimeSeriesForecaster()
    health_scorer = InfrastructureHealthScorer()
    optimization_engine = OptimizationEngine()
    routing_optimizer = RoutingOptimizer()
    anomaly_analyzer = ComplaintAnomalyAnalyzer()
    escalation_predictor = EscalationPredictor()
    
    # ============ NLP INTELLIGENCE ENDPOINTS ============
    
    @app.route('/api/ai/nlp/analyze-complaint', methods=['POST'])
    def analyze_complaint_nlp():
        """
        Analyze single complaint using NLP
        
        Request:
        {
            "complaint_id": "COMP-123",
            "description": "Road has large pothole...",
            "timestamp": "2025-05-13T10:30:00"
        }
        """
        try:
            data = request.json
            
            complaint_text = data.get('description', '')
            complaint_id = data.get('complaint_id', 'unknown')
            timestamp = datetime.fromisoformat(data.get('timestamp', datetime.now().isoformat()))
            
            analysis = nlp_pipeline.process_complaint(
                complaint_text,
                complaint_id,
                timestamp
            )
            
            return jsonify({
                'complaint_id': analysis.complaint_id,
                'classification': analysis.classification,
                'classification_confidence': analysis.classification_confidence,
                'severity_score': analysis.severity_score,
                'sentiment': analysis.sentiment_label,
                'urgency_score': analysis.urgency_score,
                'is_duplicate': analysis.is_duplicate,
                'is_fraudulent': analysis.is_fraudulent,
                'fraud_score': analysis.fraud_score,
                'summary': analysis.summary,
                'recommended_action': analysis.recommended_action
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/ai/nlp/batch-analyze', methods=['POST'])
    def batch_analyze_nlp():
        """
        Analyze batch of complaints
        
        Request:
        {
            "complaints": [
                {"complaint_id": "...", "description": "...", "timestamp": "..."},
                ...
            ]
        }
        """
        try:
            data = request.json
            complaints_list = data.get('complaints', [])
            
            # Convert to DataFrame
            df = pd.DataFrame(complaints_list)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            results = nlp_pipeline.process_batch(df)
            
            return jsonify({
                'count': len(results),
                'data': results.to_dict('records'),
                'summary': {
                    'fraudulent_count': int(results['is_fraudulent'].sum()),
                    'duplicate_count': int(results['is_duplicate'].sum()),
                    'avg_severity': float(results['severity_score'].mean()),
                    'avg_urgency': float(results['urgency_score'].mean())
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # ============ INFRASTRUCTURE FORECASTING ENDPOINTS ============
    
    @app.route('/api/ai/forecast/infrastructure-health/<ward>', methods=['GET'])
    def get_infrastructure_health(ward):
        """
        Get infrastructure health score for ward
        """
        try:
            # Mock data - in production, fetch from database
            ward_analytics = {
                'complaint_count_7d': np.random.randint(5, 20),
                'complaint_count_30d': np.random.randint(20, 80),
                'avg_complaint_age_days': np.random.randint(5, 45),
                'infrastructure_age': np.random.randint(15, 50),
                'days_since_last_repair': np.random.randint(30, 365),
                'avg_rainfall_7d': np.random.uniform(0, 30),
                'traffic_density': np.random.uniform(30, 90)
            }
            
            prediction = degradation_predictor.predict_ward_failure_probability(ward_analytics)
            
            health_score = health_scorer.calculate_health_score(
                complaint_frequency=ward_analytics['complaint_count_7d'] / 7,
                resolution_rate=0.75,
                avg_severity=0.5,
                infrastructure_age=ward_analytics['infrastructure_age'],
                maintenance_months_since=ward_analytics['days_since_last_repair'] / 30,
                environmental_risk=ward_analytics['avg_rainfall_7d'] / 50
            )
            
            return jsonify({
                'ward': ward,
                'health_score': health_score,
                'health_status': health_scorer.classify_health_status(health_score),
                'degradation_score': prediction['degradation_score'],
                'risk_level': prediction['risk_level'],
                'failure_probability': prediction['failure_probability'],
                'confidence': prediction['prediction_confidence']
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/ai/forecast/complaints/<ward>', methods=['GET'])
    def forecast_complaints(ward):
        """
        Forecast future complaint volumes
        """
        try:
            days = int(request.args.get('days', 30))
            
            # Mock historical data
            complaint_counts = np.random.randint(5, 20, size=365)
            
            forecast = forecaster.forecast_complaints(complaint_counts, days)
            
            return jsonify(forecast)
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # ============ RESOURCE OPTIMIZATION ENDPOINTS ============
    
    @app.route('/api/ai/optimization/assign-tasks', methods=['POST'])
    def assign_repair_tasks():
        """
        Assign repair tasks to workers optimally
        
        Request:
        {
            "tasks": [
                {
                    "task_id": "TASK-1",
                    "ward": "Ward 5",
                    "latitude": 12.97,
                    "longitude": 77.59,
                    "issue_type": "Pothole",
                    "urgency_score": 0.8,
                    "estimated_duration_hours": 2,
                    "required_workers": 2,
                    "estimated_cost": 5000
                }
            ],
            "workers": [...]
        }
        """
        try:
            data = request.json
            # Implementation would process tasks and workers
            # For now, return mock assignment
            
            return jsonify({
                'assignments': {},
                'total_cost': 0,
                'assignment_rate': 0.85,
                'status': 'success'
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/ai/optimization/route/<worker_id>', methods=['GET'])
    def optimize_worker_route(worker_id):
        """
        Optimize route for repair worker
        """
        try:
            # Mock route optimization
            return jsonify({
                'worker_id': worker_id,
                'route': {
                    'waypoints': [
                        {'lat': 12.97, 'lng': 77.59},
                        {'lat': 12.98, 'lng': 77.60},
                        {'lat': 12.96, 'lng': 77.58}
                    ],
                    'total_distance_km': 15.3,
                    'estimated_time_minutes': 45,
                    'efficiency_score': 0.87
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # ============ ANOMALY & FRAUD DETECTION ENDPOINTS ============
    
    @app.route('/api/ai/anomaly/check-closure/<complaint_id>', methods=['GET'])
    def check_closure_anomaly(complaint_id):
        """
        Check if complaint closure is anomalous
        """
        try:
            # Mock closure metrics
            closure_metrics = {
                'closure_time_hours': np.random.uniform(1, 100),
                'median_closure_time': 72,
                'reopening_count': np.random.randint(0, 3),
                'avg_reopening_count': 0.5,
                'severity_score': np.random.uniform(0.3, 0.9),
                'complaint_age_days': np.random.randint(1, 60)
            }
            
            result = anomaly_analyzer.analyze_complaint_closure(complaint_id, closure_metrics)
            
            return jsonify({
                'complaint_id': result.complaint_id,
                'anomaly_score': result.anomaly_score,
                'is_anomalous': result.is_anomalous,
                'anomaly_type': result.anomaly_type,
                'confidence': result.confidence,
                'reasons': result.reasons
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/ai/anomaly/systemic-issues/<ward>', methods=['GET'])
    def detect_systemic_issues(ward):
        """
        Detect systemic issues in ward
        """
        try:
            # Mock systemic issues
            return jsonify({
                'ward': ward,
                'systemic_issues': [
                    {
                        'issue_type': 'Pothole',
                        'recurring_count': 12,
                        'severity': 'high',
                        'recommendation': 'Conduct comprehensive road survey and rehabilitation'
                    }
                ]
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # ============ ESCALATION PREDICTION ENDPOINTS ============
    
    @app.route('/api/ai/escalation/predict/<complaint_id>', methods=['POST'])
    def predict_escalation(complaint_id):
        """
        Predict escalation risk for complaint
        """
        try:
            data = request.json
            
            prediction = escalation_predictor.generate_escalation_prediction(
                complaint_id,
                data
            )
            
            return jsonify({
                'complaint_id': prediction.complaint_id,
                'escalation_risk_score': prediction.escalation_risk_score,
                'escalation_probability': prediction.escalation_probability,
                'risk_level': prediction.risk_level,
                'predicted_escalation_time_days': prediction.predicted_escalation_time_days,
                'likely_escalation_channels': prediction.likely_escalation_channels,
                'contributing_factors': prediction.contributing_factors,
                'mitigation_actions': prediction.mitigation_actions
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    @app.route('/api/ai/escalation/monitor', methods=['GET'])
    def monitor_escalations():
        """
        Get escalation monitoring alerts
        """
        try:
            # Return mock escalation alerts
            return jsonify({
                'count': 3,
                'critical_count': 1,
                'high_count': 2,
                'alerts': [
                    {
                        'complaint_id': 'COMP-501',
                        'ward': 'Ward 5',
                        'risk_level': 'critical',
                        'escalation_probability': 0.92,
                        'days_until_escalation': 2,
                        'social_mentions': 247
                    }
                ]
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    # ============ DASHBOARD SUMMARY ENDPOINT ============
    
    @app.route('/api/ai/intelligence-summary', methods=['GET'])
    def get_intelligence_summary():
        """
        Get comprehensive AI intelligence summary for dashboard
        """
        try:
            return jsonify({
                'timestamp': datetime.now().isoformat(),
                'nlp_insights': {
                    'complaints_analyzed': 1245,
                    'fraudulent_detected': 23,
                    'duplicates_identified': 45,
                    'avg_severity': 0.62
                },
                'forecasting_insights': {
                    'infrastructure_health_avg': 72.3,
                    'wards_at_risk': 5,
                    'predicted_failures_7d': 8,
                    'forecast_accuracy': 0.83
                },
                'escalation_insights': {
                    'critical_escalations': 2,
                    'high_risk_complaints': 8,
                    'avg_resolution_time_hours': 48.5
                },
                'optimization_insights': {
                    'workers_deployed': 45,
                    'tasks_assigned': 87,
                    'route_efficiency_avg': 0.82,
                    'estimated_daily_cost': 145000
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400


# Function to register all AI endpoints
def register_ai_routes(app: Flask, data_path: Path = None):
    """Register all AI intelligence routes"""
    if data_path is None:
        data_path = Path(__file__).parent.parent.parent / 'data'
    
    create_intelligence_api(app, data_path)
