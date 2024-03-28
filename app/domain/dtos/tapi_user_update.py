from dataclasses import dataclass, asdict
from datetime import datetime
import app.domain.shared.shared_validation as validator
from app.domain.shared import shared_constants

@dataclass
class UserUpdateDTO:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        mobile_number: str,
        consent_preferences: dict,
    ):
        # Generate a unique user reference


        # Direct validation without preliminary checks
        validator.validate_non_empty_string(first_name, "First name")
        validator.validate_non_empty_string(last_name, "Last name")
        validator.validate_mobile_number_format(mobile_number)

        # Consent preferences validation - ensure all values are boolean and required consents are provided
        validator.validate_consent_preferences(
            consent_preferences, shared_constants.CONSENT_PREFERENCES
        )

        # Assign provided values with transformations where applicable
        self.first_name = first_name.capitalize()
        self.last_name = last_name.capitalize()
        self.mobile_number = mobile_number
        self.consent_preferences = consent_preferences
        self.created_at_timestamp=datetime.now().isoformat()
        self.updated_at_timestamp=datetime.now().isoformat()
    

    def to_json(self):
        # Use asdict to convert all fields, including Optional ones, to a dictionary
        return asdict(self)


