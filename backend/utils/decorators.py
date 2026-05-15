"""
Utility decorators for backend operations.
"""

from functools import wraps
from typing import Callable, Any
import time


def timing(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.3f} seconds")
        return result
    return wrapper


def validate_input(**validators) -> Callable:
    """
    Decorator to validate function arguments.
    
    Args:
        **validators: Argument validators
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Validation logic here
            return func(*args, **kwargs)
        return wrapper
    return decorator
