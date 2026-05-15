"""
UrbanPulse Backend Package
Smart city infrastructure management and complaint analytics platform.
"""

__version__ = "2.0.0"
__name__ = "urbanpulse_backend"

from backend.api import create_app

__all__ = ["create_app"]
