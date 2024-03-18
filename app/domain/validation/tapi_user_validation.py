from framework.error.setup.error_setup import AppError, ErrorType
import re
import uuid

# Custom marker classes for specific types of string data
class Email(str): pass
class MobileNumber(str): pass
class UKPostcode(str): pass
class UUIDStr(str): pass

def validate_non_empty_string(value: str, field_name: str = 'Value') -> None:
    if not value or not value.strip():
        display_name = field_name.replace("_", " ")  # Adjust the field name for display
        raise AppError(ErrorType.ValidationError, f"{display_name} cannot be empty or just whitespace.")

def validate_email_format(value: str, field_name: str = 'Email') -> None:
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        display_name = field_name.replace("_", " ")
        raise AppError(ErrorType.ValidationError, f"{display_name} has an invalid email format.")

def validate_mobile_number_format(value: str, field_name: str = 'MobileNumber') -> None:
    if not re.match(r"^\+[1-9]\d{1,14}$", value):
        display_name = field_name.replace("_", " ")
        raise AppError(ErrorType.ValidationError, f"{display_name} has an invalid mobile number format.")

def validate_uk_postcode_format(value: str, field_name: str = 'UKPostcode') -> None:
    postcode_pattern = r"^[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}$"
    if not re.match(postcode_pattern, value):
        display_name = field_name.replace("_", " ")
        raise AppError(ErrorType.ValidationError, f"{display_name} has an invalid UK postcode format.")

def validate_uuid_format(value: str, field_name: str = 'UUID') -> None:
    try:
        uuid.UUID(value)
    except ValueError:
        display_name = field_name.replace("_", " ")
        raise AppError(ErrorType.ValidationError, f"{display_name} has an invalid UUID format.")


class ValidationError(Exception):
    pass

class TypeBasedValidator:
    def __init__(self, rules):
        self.rules = rules

    def validate(self, data, parent_key=''):
        errors = []  # List to accumulate error messages
        self._validate(data, parent_key, errors)
        
        if errors:
            # Raise a single AppError with all accumulated errors
            raise AppError(ErrorType.ValidationError, "Validation errors occurred.", errors)

    def _validate(self, data, parent_key='', errors=[]):
        if isinstance(data, dict):
            for key, value in data.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                self._validate(value, full_key, errors)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                list_key = f"{parent_key}[{i}]"
                self._validate(item, list_key, errors)
        else:
            for data_type, validation_func in self.rules.items():
                if isinstance(data, data_type):
                    try:
                        validation_func(data, parent_key)
                    except AppError as e:
                        # Append the primary error message
                        errors.append(f"{e.errors[0]}")

# Example of how to set up validation functions to use with the validator
validator = TypeBasedValidator({
    Email: validate_email_format,
    MobileNumber: validate_mobile_number_format,
    UKPostcode: validate_uk_postcode_format,
    UUIDStr: validate_uuid_format,
    str: validate_non_empty_string,  # Now directly using validate_non_empty_string
})
