"""
Dashboard Routes
Endpoints for dashboard KPI and data retrieval.
"""

from flask import Blueprint, jsonify, request
from backend.services.dashboard_service import DashboardService

bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")
dashboard_service = DashboardService()


@bp.route("/data", methods=["GET"])
def get_dashboard_data():
    """
    Get KPI dashboard data with optional filters.
    
    Query Parameters:
        - start_date: ISO format date
        - end_date: ISO format date
        - areas: Comma-separated area names
        
    Returns:
        JSON with KPI metrics and statistics
    """
    try:
        filters = {
            "start_date": request.args.get("start_date"),
            "end_date": request.args.get("end_date"),
            "areas": request.args.get("areas", "").split(",") if request.args.get("areas") else [],
            "issue_types": request.args.get("issue_types", "").split(",") if request.args.get("issue_types") else [],
            "severity": request.args.get("severity")
        }
        
        data = dashboard_service.get_dashboard_metrics(filters)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/trends", methods=["GET"])
def get_trends():
    """
    Get complaint trend data over time.
    
    Query Parameters:
        - days: Number of days to retrieve (default: 30)
        
    Returns:
        JSON with trend data points
    """
    try:
        days = request.args.get("days", 30, type=int)
        data = dashboard_service.get_trends(days)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/summary", methods=["GET"])
def get_summary():
    """
    Get executive summary with key insights.
    
    Returns:
        JSON with summary statistics and insights
    """
    try:
        data = dashboard_service.get_summary()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/wards", methods=["GET"])
def get_ward_analytics():
    """Get analytics for all wards."""
    try:
        data = dashboard_service.get_ward_analytics()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500