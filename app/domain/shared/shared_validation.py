import re
import uuid

from app.domain.shared.shared_errors import DomainError, ErrorType


# Custom marker classes for specific types of string data
class Email(str):
    pass


class MobileNumber(str):
    pass


class UKPostcode(str):
    pass


class UUIDStr(str):
    pass


def validate_non_empty_string(value: str, field_name: str = "Value") -> None:
    if not value or not value.strip():
        display_name = field_name.replace("_", " ")  # Adjust the field name for display
        raise DomainError(
            ErrorType.ValidationError,
            f"{display_name} cannot be empty or just whitespace.",
        )
    # Check if the string is exactly one character long, regardless of its type
    if len(value.strip()) == 1:
        display_name = field_name.replace("_", " ")
        raise DomainError(
            ErrorType.ValidationError,
            f"{display_name} must not be a single character.",
        )

    trimmed_value = value.strip()
    if len(trimmed_value) == 1:
        # If the string is only one character, ensure it's not a digit or symbol
        if not re.match(r"^[a-zA-Z]$", trimmed_value):
            display_name = field_name.replace("_", " ")
            raise DomainError(
                ErrorType.ValidationError,
                f"{display_name} must not be a single number or symbol if only one character long.",
            )
    elif len(trimmed_value) < 1:
        # Ensure the string is more than one character
        display_name = field_name.replace("_", " ")
        raise DomainError(
            ErrorType.ValidationError,
            f"{display_name} must be more than one character.",
        )


def validate_email_format(value: str, display_name: str = "Email") -> None:
    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        field_name = display_name.lower().replace("_", " ")
        raise DomainError(
           ErrorType.ValidationError,errors = [{field_name:f"{display_name} has an invalid email format"}])
        


def validate_mobile_number_format(value: str, display_name: str = "MobileNumber") -> None:
    if not re.match(r"^\+[1-9]\d{1,14}$", value):
        field_name = display_name.lower().replace(" ", "_")
        raise DomainError(
            ErrorType.ValidationError,errors = [{field_name:f"{display_name} has an invalid mobile number format"}])
        


def validate_uk_postcode_format(value: str, display_name: str = "UKPostcode") -> None:
    postcode_pattern = r"^[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}$"
    if not re.match(postcode_pattern, value):
        field_name = display_name.lower().replace(" ", "_")
        raise DomainError(
             ErrorType.ValidationError,errors = [{field_name:f"{display_name} has an invalid UK postcode format"}])
        
            

def validate_uuid_format(value: str, display_name: str = "UUID") -> None:
    try:
        uuid.UUID(value)
    except ValueError:
    
        field_name = display_name.lower().replace(" ", "_")
        raise DomainError(
            ErrorType.ValidationError,errors = [{field_name:f"{display_name} has an invalid UUID format"}]
        )
        
def validate_non_empty_dict(value: dict, field_name: str = "Dictionary") -> None:
    if not value or not isinstance(value, dict) or len(value) == 0:
        display_name = field_name.replace("_", " ")  # Adjust the field name for display
        raise DomainError(
            ErrorType.ValidationError,
            f"{display_name} cannot be empty.",
        )
def validate_required_fields(dto_instance):
    errors = {}  # Dictionary to accumulate error messages
    
    for field_name, value in vars(dto_instance).items():
        # Skip fields that are not required for validation
        if field_name == "user_reference":
            continue
        if not value:  # This checks both for None and empty strings
            if field_name not in errors:
                errors[field_name] = []
            errors[field_name].append(f"{field_name.replace('_', ' ').capitalize()} is required.")

    if errors:
        raise DomainError(
            ErrorType.ValidationError, "Missing required fields.", errors
        )


def validate_consent_preferences(consent_preferences, consent_template):
    errors = {}  # Dictionary to accumulate error messages
    
    for key, is_required in consent_template.items():
        if key not in consent_preferences:
            # Missing consent
            if is_required:
                if key not in errors:
                    errors[key] = []
                errors[key].append("Missing mandatory consent")
        else:
            value = consent_preferences[key]
            if is_required and not value:
                # Mandatory consent not true
                errors.setdefault(key, []).append("Mandatory consent must be accepted")
            elif not isinstance(value, bool):
                # Consent value not boolean
                errors.setdefault(key, []).append("Must be a boolean value")
    
    # Identify unexpected consents not defined in the template
    for key in consent_preferences:
        if key not in consent_template:
            errors.setdefault(key, []).append("Unexpected consent key")

    if errors:
        raise DomainError(
            ErrorType.ValidationError, "Consent preferences validation failed", errors
        )



class ValidationException(Exception):
    pass


class TypeBasedValidator:
    def __init__(self, rules):
        self.rules = rules

    def validate(self, data, parent_key=""):
        errors = {}  # Initialize as a dict to accumulate error messages
        self._validate(data, parent_key, errors)

        if errors:
            # Raise a DomainError with all accumulated errors
            raise DomainError(
                ErrorType.ValidationError, "Validation errors occurred.", errors
            )

    def _validate(self, data, parent_key="", errors=None):
        if errors is None:
            errors = {}  # Ensure errors dict is initialized if not provided

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
                    except DomainError as e:
                        # Accumulate errors in the dict under the corresponding parent_key
                        # If the key does not exist, initialize it with a list and append the error
                        if parent_key not in errors:
                            errors[parent_key] = []
                        errors[parent_key].extend(e.errors)  # Assuming e.errors is a list of error messages



# Example of how to set up validation functions to use with the validator
validator = TypeBasedValidator(
    {
        Email: validate_email_format,
        MobileNumber: validate_mobile_number_format,
        UKPostcode: validate_uk_postcode_format,
        UUIDStr: validate_uuid_format,
        str: validate_non_empty_string,  # Now directly using validate_non_empty_string
        dict: validate_non_empty_dict
    }
)
