import uuid
from app.domain.shared import shared_constants
import app.domain.shared.shared_validation as validator


class UserCreateDTO:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        mobile_number: str,
        email: str,
        consent_preferences: dict,
    ):
        # Generate a unique user reference
        self.user_reference = str(uuid.uuid4())

        # Direct validation without preliminary checks
        validator.validate_non_empty_string(first_name, "First name")
        validator.validate_non_empty_string(last_name, "Last name")
        validator.validate_email_format(email)
        validator.validate_mobile_number_format(mobile_number)

        # Consent preferences validation - ensure all values are boolean and required consents are provided
        validator.validate_consent_preferences(
            consent_preferences, shared_constants.CONSENT_PREFERENCES
        )

        # Assign provided values with transformations where applicable
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.mobile_number = mobile_number
        self.email = email
        self.consent_preferences = consent_preferences

    def to_dict(self):
        # Converts the UserCreateDTO and its nested objects to a dictionary
        return {
            "user_reference": self.user_reference,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "mobile_number": self.mobile_number,
            "email": self.email,
            "consent_preferences": self.consent_preferences,
        }
