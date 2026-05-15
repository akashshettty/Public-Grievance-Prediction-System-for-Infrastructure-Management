"""
Input validators for API endpoints.
"""

from typing import Any, Optional, List


def validate_string(value: Any, min_length: int = 1, max_length: int = 1000) -> bool:
    """
    Validate string input.
    
    Args:
        value: Value to validate
        min_length: Minimum length
        max_length: Maximum length
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(value, str):
        return False
    return min_length <= len(value) <= max_length


def validate_integer(value: Any, min_val: int = 0, max_val: int = 1000000) -> bool:
    """
    Validate integer input.
    
    Args:
        value: Value to validate
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        True if valid, False otherwise
    """
    try:
        num = int(value)
        return min_val <= num <= max_val
    except (ValueError, TypeError):
        return False


def validate_list(value: Any, item_type: type = None) -> bool:
    """
    Validate list input.
    
    Args:
        value: Value to validate
        item_type: Expected type of items in list
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(value, list):
        return False
    
    if item_type is None:
        return True
    
    return all(isinstance(item, item_type) for item in value)
