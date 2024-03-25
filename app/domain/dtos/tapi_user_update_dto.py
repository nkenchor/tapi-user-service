from dataclasses import dataclass,  asdict
from typing import Optional
import app.domain.shared.shared_validation as validator


@dataclass
class UserUpdateDTO:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[str] = None

    def __post_init__(self):
        validator.validate_non_empty_string(self.first_name, "First name")
        validator.validate_non_empty_string(self.last_name, "Last name")
        validator.validate_email_format(self.email)
        validator.validate_mobile_number_format(self.mobile_number)
        
    def to_dict(self):
        return asdict(self)
