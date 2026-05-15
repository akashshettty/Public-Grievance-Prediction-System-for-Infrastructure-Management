"""API routes package."""

from . import health_routes
from . import dashboard_routes
from . import ai_routes
from . import complaint_routes

__all__ = [
    "health_routes",
    "dashboard_routes",
    "ai_routes",
    "complaint_routes"
]
