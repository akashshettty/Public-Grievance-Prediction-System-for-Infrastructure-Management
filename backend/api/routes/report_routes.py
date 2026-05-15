
from flask import Blueprint, jsonify, request
from backend.services.report_service import ReportService

bp = Blueprint("reports", __name__, url_prefix="/api/reports")
report_service = ReportService()

@bp.route("/generate", methods=["POST"])
def generate_report():
    """
    Generate a new report.
    """
    try:
        data = request.json or {}
        report_type = data.get("type", "Executive Summary")
        title = data.get("title", "")
        ward = data.get("ward")
        
        report = report_service.generate_report(report_type, title, ward)
        return jsonify(report), 200
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@bp.route("", methods=["GET"])
def get_reports():
    """
    Get list of available reports (simulated).
    """
    return jsonify({
        "reports": [
            {
                "id": "1",
                "title": "Monthly Executive Summary - May 2025",
                "date": "May 30, 2025",
                "type": "Executive Report"
            }
        ]
    }), 200
