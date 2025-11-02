"""
Input validation utilities for student registration and attendance.
Ensures data integrity and security throughout the application.
"""

import re
from typing import Tuple, List
from datetime import datetime


class ValidationError(Exception):
    """Custom exception for validation errors"""

    pass


class StudentValidator:
    """Validate student registration inputs"""

    # Regex patterns
    ENROLLMENT_PATTERN = re.compile(r"^[A-Z0-9]{3,20}$")
    NAME_PATTERN = re.compile(r"^[a-zA-Z\s]{2,50}$")
    SUBJECT_PATTERN = re.compile(r"^[a-zA-Z0-9\s\-]{2,100}$")

    @staticmethod
    def validate_enrollment(enrollment: str) -> Tuple[bool, str]:
        """
        Validate student enrollment number.

        Args:
            enrollment (str): Student enrollment number

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not enrollment:
            return False, "Enrollment number cannot be empty"

        if len(enrollment) < 3 or len(enrollment) > 20:
            return False, "Enrollment number must be between 3 and 20 characters"

        if not StudentValidator.ENROLLMENT_PATTERN.match(enrollment):
            return False, "Enrollment must contain only letters and numbers"

        return True, ""

    @staticmethod
    def validate_name(name: str) -> Tuple[bool, str]:
        """
        Validate student name.

        Args:
            name (str): Student name

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not name:
            return False, "Name cannot be empty"

        if len(name) < 2 or len(name) > 50:
            return False, "Name must be between 2 and 50 characters"

        if not StudentValidator.NAME_PATTERN.match(name):
            return False, "Name can only contain letters and spaces"

        return True, ""

    @staticmethod
    def validate_subject(subject: str) -> Tuple[bool, str]:
        """
        Validate subject name.

        Args:
            subject (str): Subject name

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not subject:
            return False, "Subject name cannot be empty"

        if len(subject) < 2 or len(subject) > 100:
            return False, "Subject name must be between 2 and 100 characters"

        if not StudentValidator.SUBJECT_PATTERN.match(subject):
            return False, "Subject name contains invalid characters"

        return True, ""

    @staticmethod
    def validate_student_registration(
        enrollment: str, name: str
    ) -> Tuple[bool, List[str]]:
        """
        Validate complete student registration data.

        Args:
            enrollment (str): Student enrollment number
            name (str): Student name

        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []

        enrollment_valid, enrollment_error = StudentValidator.validate_enrollment(
            enrollment
        )
        if not enrollment_valid:
            errors.append(enrollment_error)

        name_valid, name_error = StudentValidator.validate_name(name)
        if not name_valid:
            errors.append(name_error)

        return len(errors) == 0, errors


class DateValidator:
    """Validate date-related inputs"""

    @staticmethod
    def validate_date_format(date_str: str, format: str = "%Y-%m-%d") -> bool:
        """
        Validate date string format.

        Args:
            date_str (str): Date string
            format (str): Expected format

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, str]:
        """
        Validate date range (start <= end).

        Args:
            start_date (str): Start date string
            end_date (str): End date string

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            if start > end:
                return False, "Start date must be before end date"

            return True, ""
        except ValueError:
            return False, "Invalid date format"


# Example usage
if __name__ == "__main__":
    # Test enrollment validation
    is_valid, error = StudentValidator.validate_enrollment("CSE2024")
    print(f"Enrollment validation: {is_valid} - {error}")

    # Test name validation
    is_valid, error = StudentValidator.validate_name("John Doe")
    print(f"Name validation: {is_valid} - {error}")

    # Test complete registration
    is_valid, errors = StudentValidator.validate_student_registration(
        "CSE2024", "John Doe"
    )
    print(f"Complete registration: {is_valid} - {errors}")
