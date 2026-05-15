"""
UrbanPulse Backend API Package
Handles all API routes and endpoints.
"""

from flask import Flask
from flask_cors import CORS
from backend.config import get_config

def create_app(config=None):
    """
    Factory function to create and configure Flask application.
    
    Args:
        config: Configuration object (uses environment config if None)
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config()
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app, origins=app.config["CORS_ORIGINS"])
    
    # Register blueprints
    from backend.api.routes import (
        health_routes,
        dashboard_routes,
        ai_routes,
        complaint_routes,
        report_routes
    )
    
    app.register_blueprint(health_routes.bp)
    app.register_blueprint(dashboard_routes.bp)
    app.register_blueprint(ai_routes.bp)
    app.register_blueprint(complaint_routes.bp)
    app.register_blueprint(report_routes.bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Endpoint not found"}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        return {"error": "Internal server error"}, 500
    
    return app
