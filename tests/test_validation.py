import pytest
from datetime import datetime
from src.validation import (
    validate_email,
    validate_datetime,
    validate_task_name,
    validate_description
)


class TestEmailValidation:
    def test_valid_emails(self):
        """Test valid email addresses."""
        assert validate_email("test@example.com") is True
        assert validate_email("user.name@domain.co.uk") is True
        assert validate_email("user+tag@example.org") is True
    
    def test_invalid_emails(self):
        """Test invalid email addresses."""
        assert validate_email("invalid") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False
        assert validate_email("user @example.com") is False
        assert validate_email("") is False


class TestDatetimeValidation:
    def test_valid_datetime(self):
        """Test valid datetime strings."""
        is_valid, dt = validate_datetime("2023-12-31T23:59:59")
        assert is_valid is True
        assert dt == datetime(2023, 12, 31, 23, 59, 59)
        
        is_valid, dt = validate_datetime("2024-01-01T00:00:00")
        assert is_valid is True
    
    def test_invalid_datetime(self):
        """Test invalid datetime strings."""
        is_valid, dt = validate_datetime("invalid")
        assert is_valid is False
        assert dt is None
        
        is_valid, dt = validate_datetime("2023-13-01T00:00:00")  # Invalid month
        assert is_valid is False
        
        is_valid, dt = validate_datetime("")
        assert is_valid is False


class TestTaskNameValidation:
    def test_valid_names(self):
        """Test valid task names."""
        assert validate_task_name("Valid Task") is True
        assert validate_task_name("Task 123") is True
        assert validate_task_name("A" * 200) is True  # Max length
    
    def test_invalid_names(self):
        """Test invalid task names."""
        assert validate_task_name("") is False
        assert validate_task_name("   ") is False  # Only whitespace
        assert validate_task_name("A" * 201) is False  # Too long
        assert validate_task_name(None) is False
        assert validate_task_name(123) is False  # Not a string


class TestDescriptionValidation:
    def test_valid_descriptions(self):
        """Test valid descriptions."""
        assert validate_description("Valid description") is True
        assert validate_description("") is True  # Empty is allowed
        assert validate_description("A" * 1000) is True  # Max length
    
    def test_invalid_descriptions(self):
        """Test invalid descriptions."""
        assert validate_description("A" * 1001) is False  # Too long
        assert validate_description(None) is False
        assert validate_description(123) is False  # Not a string
