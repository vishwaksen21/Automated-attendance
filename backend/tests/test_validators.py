"""
Unit tests for input validation.
Run with: pytest backend/tests/test_validators.py -v
"""

import pytest
from backend.utils.validators import StudentValidator, DateValidator


class TestStudentValidator:
    """Test cases for StudentValidator"""

    # ==================== Enrollment Tests ====================

    def test_valid_enrollment(self):
        """Test valid enrollment number"""
        is_valid, error = StudentValidator.validate_enrollment("CSE2024")
        assert is_valid is True
        assert error == ""

    def test_enrollment_empty(self):
        """Test empty enrollment"""
        is_valid, error = StudentValidator.validate_enrollment("")
        assert is_valid is False
        assert "cannot be empty" in error.lower()

    def test_enrollment_too_short(self):
        """Test enrollment with less than 3 characters"""
        is_valid, error = StudentValidator.validate_enrollment("AB")
        assert is_valid is False

    def test_enrollment_too_long(self):
        """Test enrollment with more than 20 characters"""
        is_valid, error = StudentValidator.validate_enrollment("A" * 25)
        assert is_valid is False

    def test_enrollment_with_special_chars(self):
        """Test enrollment with special characters"""
        is_valid, error = StudentValidator.validate_enrollment("CSE@2024")
        assert is_valid is False

    def test_enrollment_lowercase(self):
        """Test enrollment with lowercase letters"""
        is_valid, error = StudentValidator.validate_enrollment("cse2024")
        assert is_valid is False

    # ==================== Name Tests ====================

    def test_valid_name(self):
        """Test valid name"""
        is_valid, error = StudentValidator.validate_name("John Doe")
        assert is_valid is True
        assert error == ""

    def test_name_empty(self):
        """Test empty name"""
        is_valid, error = StudentValidator.validate_name("")
        assert is_valid is False
        assert "cannot be empty" in error.lower()

    def test_name_single_character(self):
        """Test name with single character"""
        is_valid, error = StudentValidator.validate_name("A")
        assert is_valid is False

    def test_name_with_numbers(self):
        """Test name containing numbers"""
        is_valid, error = StudentValidator.validate_name("John123")
        assert is_valid is False

    def test_name_with_special_chars(self):
        """Test name with special characters"""
        is_valid, error = StudentValidator.validate_name("John@Doe")
        assert is_valid is False

    def test_name_multiple_spaces(self):
        """Test name with multiple spaces"""
        is_valid, error = StudentValidator.validate_name("John    Doe")
        # This might be valid depending on requirements
        # Adjust assertion based on your needs
        pass

    # ==================== Subject Tests ====================

    def test_valid_subject(self):
        """Test valid subject name"""
        is_valid, error = StudentValidator.validate_subject("Mathematics-101")
        assert is_valid is True
        assert error == ""

    def test_subject_empty(self):
        """Test empty subject"""
        is_valid, error = StudentValidator.validate_subject("")
        assert is_valid is False

    def test_subject_with_numbers(self):
        """Test subject with numbers"""
        is_valid, error = StudentValidator.validate_subject("Physics 101")
        assert is_valid is True

    def test_subject_too_long(self):
        """Test subject with more than 100 characters"""
        is_valid, error = StudentValidator.validate_subject("A" * 101)
        assert is_valid is False

    # ==================== Complete Registration Tests ====================

    def test_valid_registration(self):
        """Test valid registration data"""
        is_valid, errors = StudentValidator.validate_student_registration(
            "CSE2024", "John Doe"
        )
        assert is_valid is True
        assert errors == []

    def test_registration_invalid_enrollment(self):
        """Test registration with invalid enrollment"""
        is_valid, errors = StudentValidator.validate_student_registration(
            "invalid!", "John Doe"
        )
        assert is_valid is False
        assert len(errors) > 0

    def test_registration_invalid_name(self):
        """Test registration with invalid name"""
        is_valid, errors = StudentValidator.validate_student_registration(
            "CSE2024", "John123"
        )
        assert is_valid is False
        assert len(errors) > 0

    def test_registration_both_invalid(self):
        """Test registration with both invalid"""
        is_valid, errors = StudentValidator.validate_student_registration(
            "invalid!", "Invalid123"
        )
        assert is_valid is False
        assert len(errors) == 2


class TestDateValidator:
    """Test cases for DateValidator"""

    def test_valid_date_format(self):
        """Test valid date format"""
        is_valid = DateValidator.validate_date_format("2024-10-31")
        assert is_valid is True

    def test_invalid_date_format(self):
        """Test invalid date format"""
        is_valid = DateValidator.validate_date_format("31/10/2024")
        assert is_valid is False

    def test_date_range_valid(self):
        """Test valid date range"""
        is_valid, error = DateValidator.validate_date_range(
            "2024-10-01", "2024-10-31"
        )
        assert is_valid is True
        assert error == ""

    def test_date_range_same_dates(self):
        """Test date range with same start and end"""
        is_valid, error = DateValidator.validate_date_range(
            "2024-10-31", "2024-10-31"
        )
        assert is_valid is True

    def test_date_range_invalid(self):
        """Test invalid date range (start after end)"""
        is_valid, error = DateValidator.validate_date_range(
            "2024-10-31", "2024-10-01"
        )
        assert is_valid is False
        assert "before" in error.lower()

    def test_date_range_invalid_format(self):
        """Test date range with invalid format"""
        is_valid, error = DateValidator.validate_date_range(
            "31/10/2024", "01/10/2024"
        )
        assert is_valid is False


# Run tests with coverage
# pytest backend/tests/test_validators.py -v --cov=backend.utils.validators
