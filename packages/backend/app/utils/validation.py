import re
from typing import Optional
from pydantic import validator


def validate_email(email: str) -> bool:
    """
    Validate email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> bool:
    """
    Validate password strength
    At least 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character
    """
    if len(password) < 8:
        return False

    has_upper = re.search(r'[A-Z]', password) is not None
    has_lower = re.search(r'[a-z]', password) is not None
    has_digit = re.search(r'\d', password) is not None
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password) is not None

    return has_upper and has_lower and has_digit and has_special


def sanitize_input(input_str: str) -> str:
    """
    Sanitize input string to prevent injection attacks
    """
    if input_str is None:
        return ""

    # Remove potentially dangerous characters
    sanitized = input_str.strip()
    # Prevent potential script tags and other dangerous content
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)

    return sanitized


def validate_title(title: str) -> bool:
    """
    Validate todo title
    """
    if not title or len(title.strip()) == 0:
        return False

    if len(title) > 255:
        return False

    return True


def validate_description(description: Optional[str]) -> bool:
    """
    Validate todo description
    """
    if description is None:
        return True

    if len(description) > 1000:  # Limit description length
        return False

    return True