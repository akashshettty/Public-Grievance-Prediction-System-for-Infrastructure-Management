"""
Health Check Routes
Endpoints for system health and status monitoring.
"""

from flask import Blueprint, jsonify
from datetime import datetime

bp = Blueprint("health", __name__, url_prefix="/api/health")


@bp.route("", methods=["GET"])
def health_check():
    """
    System health check endpoint.
    
    Returns:
        JSON with status and timestamp
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    }), 200


@bp.route("/ready", methods=["GET"])
def readiness_check():
    """
    Readiness check endpoint for orchestration.
    
    Returns:
        JSON with readiness status
    """
    return jsonify({
        "ready": True,
        "timestamp": datetime.now().isoformat()
    }), 200


@bp.route("/live", methods=["GET"])
def liveness_check():
    """
    Liveness check endpoint for orchestration.
    
    Returns:
        JSON with liveness status
    """
    return jsonify({
        "alive": True,
        "timestamp": datetime.now().isoformat()
    }), 200
