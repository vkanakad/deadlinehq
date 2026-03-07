"""Input validation utilities for DeadlineHQ."""
from datetime import datetime
import re


def validate_email(email: str) -> bool:
    """Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_datetime(datetime_str: str) -> tuple[bool, datetime | None]:
    """Validate and parse datetime string in ISO format.
    
    Args:
        datetime_str: Datetime string to validate
        
    Returns:
        Tuple of (is_valid, parsed_datetime or None)
    """
    try:
        dt = datetime.fromisoformat(datetime_str)
        return True, dt
    except (ValueError, TypeError):
        return False, None


def validate_task_name(name: str) -> bool:
    """Validate task name.
    
    Args:
        name: Task name to validate
        
    Returns:
        True if name is valid, False otherwise
    """
    if not name or not isinstance(name, str):
        return False
    if len(name.strip()) == 0:
        return False
    if len(name) > 200:
        return False
    return True


def validate_description(description: str) -> bool:
    """Validate task description.
    
    Args:
        description: Description to validate
        
    Returns:
        True if description is valid, False otherwise
    """
    if not isinstance(description, str):
        return False
    if len(description) > 1000:
        return False
    return True
