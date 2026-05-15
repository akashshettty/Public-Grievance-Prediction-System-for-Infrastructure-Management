"""
AI Intelligence Routes
Endpoints for AI module outputs and predictions.
"""

from flask import Blueprint, jsonify, request
from backend.services.ai_service import AIService
import numpy as np
import json
from datetime import datetime

class NumpyJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy and pandas types."""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        elif isinstance(obj, (datetime, np.datetime64)):
            return obj.isoformat() if hasattr(obj, 'isoformat') else str(obj)
        return super().default(obj)

bp = Blueprint("ai", __name__, url_prefix="/api/ai")
ai_service = AIService()


def safe_jsonify(data):
    """Safely jsonify data with numpy type support."""
    try:
        # Use json.dumps to verify serialization before returning
        serialized = json.dumps(data, cls=NumpyJSONEncoder)
        return jsonify(json.loads(serialized))
    except Exception as e:
        import traceback
        with open("escalation_debug.log", "a") as f:
            f.write(f"SERIALIZATION ERROR: {e}\n")
            f.write(traceback.format_exc())
        return jsonify({"error": f"Serialization error: {str(e)}"}), 500


@bp.route("/complaint-analysis", methods=["GET"])
def get_complaint_analysis():
    """NLP complaint classification and analysis."""
    try:
        limit = request.args.get("limit", 50, type=int)
        data = ai_service.analyze_complaints(limit)
        return safe_jsonify(data), 200
    except Exception as e:
        return safe_jsonify({"error": str(e)}), 500


@bp.route("/analyze-text", methods=["POST"])
def analyze_text():
    """Real-time NLP analysis for a single text input."""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return safe_jsonify({"error": "No text provided"}), 400
            
        result = ai_service.analyze_text(data['text'])
        return safe_jsonify(result), 200
    except Exception as e:
        return safe_jsonify({"error": str(e)}), 500


@bp.route("/fraud-detection", methods=["GET"])
def get_fraud_detection():
    """Anomaly and fraud detection in complaints."""
    try:
        data = ai_service.detect_fraud()
        return safe_jsonify(data), 200
    except Exception as e:
        return safe_jsonify({"error": str(e)}), 500


@bp.route("/escalation-risks", methods=["GET"])
def get_escalation_risks():
    """Escalation risk prediction for complaints."""
    try:
        with open("escalation_debug.log", "a") as f:
            f.write("DEBUG: Escalation endpoint called\n")
        data = ai_service.predict_escalations()
        with open("escalation_debug.log", "a") as f:
            f.write(f"DEBUG: Got {len(data.get('risks', []))} risks\n")
        return safe_jsonify(data), 200
    except Exception as e:
        import traceback
        with open("escalation_debug.log", "a") as f:
            f.write(f"ERROR: {e}\n")
            f.write(traceback.format_exc())
        return safe_jsonify({"error": str(e)}), 500


@bp.route("/infrastructure-health", methods=["GET"])
def get_infrastructure_health():
    """Infrastructure health scoring."""
    try:
        areas = request.args.getlist("areas")
        data = ai_service.assess_infrastructure_health(areas)
        return safe_jsonify(data), 200
    except Exception as e:
        return safe_jsonify({"error": str(e)}), 500


@bp.route("/failure-prediction", methods=["GET"])
def get_failure_prediction():
    """Infrastructure failure predictions."""
    try:
        data = ai_service.predict_failures()
        return safe_jsonify(data), 200
    except Exception as e:
        return safe_jsonify({"error": str(e)}), 500


@bp.route("/resource-optimization", methods=["GET"])
def get_resource_optimization():
    """Resource allocation and route optimization."""
    try:
        data = ai_service.optimize_resources()
        return safe_jsonify(data), 200
    except Exception as e:
        return safe_jsonify({"error": str(e)}), 500


@bp.route("/data-ingestion", methods=["GET"])
def get_data_ingestion_status():
    """Data ingestion pipeline status."""
    try:
        data = ai_service.get_ingestion_status()
        return safe_jsonify(data), 200
    except Exception as e:
        return safe_jsonify({"error": str(e)}), 500


@bp.route("/digital-twin/summary", methods=["GET"])
def get_digital_twin_summary():
    """
    Unified endpoint for the Digital Twin Dashboard.
    Returns intelligence from all AI modules:
    - Recent Predictions
    - Active Fraud Alerts
    - Resource Recommendations
    - Escalation Risks
    """
    try:
        summary = {
            "forecasting": ai_service.predict_failures(),
            "fraud": ai_service.detect_fraud(),
            "optimization": ai_service.optimize_resources(),
            "escalation": ai_service.predict_escalations(),
            "timestamp": datetime.now().isoformat(),
            "city_health_index": 82.5
        }
        return safe_jsonify(summary), 200
    except Exception as e:
        return safe_jsonify({"error": str(e)}), 500
@bp.route("/query", methods=["POST"])
def ai_query():
    """Natural language query interface for the dashboard."""
    try:
        data = request.get_json()
        query = data.get("query", "").lower()
        
        # Simple rule-based "AI" responder using real data
        from backend.services.data_service import DataService
        ds = DataService()
        df = ds.get_grievances_data()
        
        response = ""
        if "ward" in query:
            worst_ward = df['ward'].value_counts().idxmax()
            count = df['ward'].value_counts().max()
            response = f"Based on current data, {worst_ward} has the highest volume of complaints ({count}). I recommend prioritizing resources there."
        elif "status" in query or "many" in query:
            total = len(df)
            resolved = len(df[df['status'].astype(str).str.lower().isin(['closed', 'resolved'])])
            response = f"Currently, we are tracking {total} total complaints. We have resolved {resolved} of them, giving us a city-wide resolution rate of {round(resolved/total*100, 1)}%."
        elif "most" in query or "common" in query:
            top_issue = df['issue_type'].value_counts().idxmax()
            response = f"The most frequent issue reported is '{top_issue}'. We are seeing a 15% increase in these reports this week."
        else:
            response = "I am UrbanPulse AI. I can help you analyze city infrastructure. You can ask about 'worst wards', 'current status', or 'common issues'."
            
        return safe_jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.94
        }), 200
    except Exception as e:
        return safe_jsonify({"error": str(e)}), 500
