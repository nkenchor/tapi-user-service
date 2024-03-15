import re

from frameworks_and_drivers.error.config.error_setup import AppError, ErrorType


def validate_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise AppError(ErrorType.ValidationError, f"{field_name} cannot be empty or just whitespace.")

def validate_email_format(email: str) -> None:
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        raise AppError(ErrorType.InvalidEmailFormat, "Invalid email format.")

def validate_mobile_number_format(mobile_number: str) -> None:
    if not re.match(r"^\+[1-9]\d{1,14}$", mobile_number):
        raise AppError(ErrorType.InvalidMobileNumberFormat, "Invalid mobile number format.")
