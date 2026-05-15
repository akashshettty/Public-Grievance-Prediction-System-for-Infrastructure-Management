"""
Helper functions for backend operations.
"""

from typing import Any, Dict, List
from datetime import datetime, timedelta
import pandas as pd


def parse_date(date_str: str) -> datetime:
    """
    Parse ISO format date string.
    
    Args:
        date_str: Date string in ISO format
        
    Returns:
        Datetime object
    """
    try:
        return datetime.fromisoformat(date_str)
    except (ValueError, TypeError):
        return None


def date_range_filter(start_date: str = None, end_date: str = None) -> tuple:
    """
    Parse and validate date range.
    
    Args:
        start_date: Start date string
        end_date: End date string
        
    Returns:
        Tuple of (start_datetime, end_datetime)
    """
    start = parse_date(start_date) if start_date else datetime.now() - timedelta(days=30)
    end = parse_date(end_date) if end_date else datetime.now()
    
    return start, end


def serialize_datetime(obj: Any) -> Any:
    """
    JSON serialize datetime objects.
    
    Args:
        obj: Object to serialize
        
    Returns:
        Serialized object
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj
