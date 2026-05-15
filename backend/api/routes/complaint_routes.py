"""
Complaint Routes
Endpoints for complaint data retrieval and management.
"""

from flask import Blueprint, jsonify, request
from backend.services.complaint_service import ComplaintService

bp = Blueprint("complaints", __name__, url_prefix="/api/complaints")
complaint_service = ComplaintService()


@bp.route("", methods=["GET"])
def get_complaints():
    """
    Get complaints with optional filtering.
    
    Query Parameters:
        - status: Complaint status (open, closed, etc.)
        - area: Filter by area/ward
        - issue_type: Filter by issue type
        - limit: Number of results (default: 100)
        - offset: Pagination offset (default: 0)
        
    Returns:
        JSON with complaint records and count
    """
    try:
        filters = {
            "status": request.args.get("status"),
            "area": request.args.get("area"),
            "issue_type": request.args.get("issue_type"),
            "limit": request.args.get("limit", 100, type=int),
            "offset": request.args.get("offset", 0, type=int)
        }
        
        data = complaint_service.get_complaints(filters)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<complaint_id>", methods=["GET"])
def get_complaint_detail(complaint_id):
    """
    Get detailed information about a specific complaint.
    
    Args:
        complaint_id: Unique complaint identifier
        
    Returns:
        JSON with complaint details
    """
    try:
        data = complaint_service.get_complaint(complaint_id)
        if data:
            return jsonify(data), 200
        return jsonify({"error": "Complaint not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/statistics", methods=["GET"])
def get_complaint_statistics():
    """
    Get complaint statistics and aggregations.
    
    Query Parameters:
        - group_by: Group by status, area, or issue_type
        
    Returns:
        JSON with statistical aggregations
    """
    try:
        group_by = request.args.get("group_by", "status")
        data = complaint_service.get_statistics(group_by)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
