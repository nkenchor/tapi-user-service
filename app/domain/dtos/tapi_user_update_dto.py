from dataclasses import dataclass, asdict
from typing import Optional
import app.domain.shared.shared_validation as validator


@dataclass
class UserUpdateDTO:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[str] = None
    consent_preferences: Optional[dict] = None

    def __post_init__(self):
        # Ensure first_name and last_name start with a capital letter if they are provided

        self.first_name = self.first_name.capitalize()
        validator.validate_non_empty_string(self.first_name, "First name")

        self.last_name = self.last_name.capitalize()
        validator.validate_non_empty_string(self.last_name, "Last name")

        validator.validate_email_format(self.email)

        validator.validate_mobile_number_format(self.mobile_number)

        validator.validate_consent_preferences(
            self.consent_preferences, "Consent preference"
        )

    def to_dict(self):
        # Use asdict to convert all fields, including Optional ones, to a dictionary
        return asdict(self)
